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

