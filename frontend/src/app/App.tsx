import { ApolloProvider } from "@apollo/client";

import { QuotePage } from "../features/quote/QuotePage";
import { apolloClient } from "../graphql/client";
import "../styles/app.css";

const App = () => {
  return (
    <ApolloProvider client={apolloClient}>
      <QuotePage />
    </ApolloProvider>
  );
};

export default App;
