import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Fonction pour charger les données de chaque titre dans le portefeuille
def load_portfolio_data(tickers, quantities, start_date, end_date):
    portfolio_data = {}
    for ticker, quantity in zip(tickers, quantities):
        # Télécharge les données et vérifie si elles existent
        data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        if data.empty:
            st.error(f"Impossible de récupérer des données pour le ticker {ticker}. Vérifiez qu'il est correct.")
            return None  # Retourne None si les données sont manquantes
        portfolio_data[ticker] = data * quantity  # Multiplie par le nombre d'actions détenues
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_daily_value = portfolio_df.sum(axis=1)  # Somme pour avoir la valeur quotidienne totale du portefeuille
    return portfolio_daily_value

# Fonction pour télécharger les données de l'indice
def download_index_data(index_symbol, start_date, end_date):
    index_data = yf.download(index_symbol, start=start_date, end=end_date)
    index_data = index_data['Adj Close']
    return index_data

# Fonction pour calculer le retour cumulatif
def calculate_cumulative_return(data):
    return (data / data.iloc[0]) - 1

# Fonction pour calculer la volatilité
def calculate_volatility(data):
    daily_returns = data.pct_change().dropna()
    return daily_returns.std() * np.sqrt(252)  # Volatilité annualisée

# Fonction principale de l'application Streamlit
def main():
    st.title("Comparaison de Portefeuille avec Indice de Référence")

    # Saisie des informations du portefeuille
    st.sidebar.header("Entrer votre portefeuille")
    tickers = st.sidebar.text_input("Entrer les tickers séparés par des virgules (ex: AAPL, MSFT, VTI)")
    quantities = st.sidebar.text_input("Entrer les quantités correspondantes séparées par des virgules (ex: 10, 15, 20)")

    # Sélection de l'indice de référence
    index_symbol = st.sidebar.selectbox(
        "Sélectionnez l'indice de référence", 
        options=["^GSPC", "^DJI", "^IXIC"],  # Exemples : S&P 500 (^GSPC), Dow Jones (^DJI), Nasdaq (^IXIC)
    )

    # Période d’analyse
    start_date = st.sidebar.date_input("Date de début", value=pd.to_datetime("2022-01-01"))
    end_date = st.sidebar.date_input("Date de fin", value=pd.to_datetime("today"))

    # Vérifie si les tickers et les quantités ont été fournis
    if tickers and quantities:
        try:
            tickers = [ticker.strip() for ticker in tickers.split(',')]
            quantities = [float(quantity.strip()) for quantity in quantities.split(',')]

            # Vérifie que le nombre de tickers correspond au nombre de quantités
            if len(tickers) != len(quantities):
                st.error("Le nombre de tickers doit correspondre au nombre de quantités. Veuillez vérifier les deux champs.")
                return

            # Chargement des données de portefeuille
            portfolio_daily_value = load_portfolio_data(tickers, quantities, start_date, end_date)
            if portfolio_daily_value is None:
                return  # Arrête l'exécution si un ticker est invalide

            # Téléchargement des données de l'indice
            index_data = download_index_data(index_symbol, start_date, end_date)

            # Alignement des données sur les mêmes dates
            combined_data = pd.DataFrame({
                "Portfolio": portfolio_daily_value,
                "Index": index_data
            }).dropna()

            # Calculs de performance
            portfolio_return = calculate_cumulative_return(combined_data["Portfolio"])
            index_return = calculate_cumulative_return(combined_data["Index"])
            
            portfolio_volatility = calculate_volatility(combined_data["Portfolio"])
            index_volatility = calculate_volatility(combined_data["Index"])

            # Affichage des résultats
            st.subheader("Comparaison des Performances")
            st.write(f"Retour cumulatif du portefeuille: {portfolio_return.iloc[-1]:.2%}")
            st.write(f"Retour cumulatif de l'indice: {index_return.iloc[-1]:.2%}")
            st.write(f"Volatilité du portefeuille: {portfolio_volatility:.2%}")
            st.write(f"Volatilité de l'indice: {index_volatility:.2%}")

            # Graphique des retours cumulés
            st.subheader("Graphique des retours cumulés")
            plt.figure(figsize=(10, 6))
            plt.plot(portfolio_return, label="Portefeuille")
            plt.plot(index_return, label="Indice de Référence")
            plt.xlabel("Date")
            plt.ylabel("Retour Cumulatif")
            plt.legend()
            st.pyplot(plt)

        except ValueError:
            st.error("Erreur de format : assurez-vous que les quantités sont bien des nombres et que les tickers sont valides.")

if __name__ == "__main__":
    main()

