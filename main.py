class DataFetcher:
    def fetch_data(self):
        pass


class PSEDataFetcher(DataFetcher):
    def fetch_data(self):
        # Implement the data fetching logic for PSE here
        print("Fetching data from Polskie Sieci Energetyczne (PSE)")


class TGEDataFetcher(DataFetcher):
    def fetch_data(self):
        # Implement the data fetching logic for TGE here
        print("Fetching data from Towarowa Giełda Energii (TGE)")


class DataFetcherFactory:
    def create_data_fetcher(self, source):
        if source == "PSE":
            return PSEDataFetcher()
        elif source == "TGE":
            return TGEDataFetcher()
        else:
            raise ValueError("Invalid source specified")


if __name__ == "__main__":
    # Example usage:
    data_fetcher_factory = DataFetcherFactory()

    # Create a PSE data fetcher
    pse_fetcher = data_fetcher_factory.create_data_fetcher("PSE")
    pse_fetcher.fetch_data()

    # Create a TGE data fetcher
    tge_fetcher = data_fetcher_factory.create_data_fetcher("TGE")
    tge_fetcher.fetch_data()
