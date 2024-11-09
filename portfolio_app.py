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
