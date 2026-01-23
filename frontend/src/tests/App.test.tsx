import { render, screen } from "@testing-library/react";

import App from "../app/App";

jest.mock("../infrastructure/graphql/quoteGateway", () => ({
  createQuoteGateway: () => ({
    getStates: jest.fn(),
    getQuote: jest.fn(),
  }),
}));

jest.mock("../features/quote/QuotePage", () => ({
  QuotePage: () => <div>Quote Page</div>,
}));

describe("App", () => {
  it("renders the quote page", () => {
    render(<App />);
    expect(screen.getByText("Quote Page")).toBeInTheDocument();
  });
});
