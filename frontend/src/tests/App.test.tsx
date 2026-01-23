import { render, screen } from "@testing-library/react";

import App from "../app/App";

jest.mock("../graphql/client", () => ({
  apolloClient: {
    query: jest.fn(),
    mutate: jest.fn(),
    watchQuery: jest.fn(),
  },
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
