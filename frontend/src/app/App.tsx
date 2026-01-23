import { QuotePage } from "../features/quote/QuotePage";
import { createQuoteGateway } from "../infrastructure/graphql/quoteGateway";
import "../styles/app.css";

const quoteGateway = createQuoteGateway();

const App = () => {
  return <QuotePage quoteGateway={quoteGateway} />;
};

export default App;
