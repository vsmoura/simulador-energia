import { ApolloClient, NormalizedCacheObject } from "@apollo/client";

import { QuoteGateway } from "../../application/quote/ports";
import { QuoteResult, StateOption } from "../../domain/quote/types";
import { apolloClient } from "./client";
import { QUOTE_QUERY, STATES_QUERY } from "./queries";

interface QuoteResponse {
  quote: QuoteResult;
}

interface StatesResponse {
  states: StateOption[];
}

export const createQuoteGateway = (
  client: ApolloClient<NormalizedCacheObject> = apolloClient,
): QuoteGateway => ({
  async getStates() {
    const { data } = await client.query<StatesResponse>({
      query: STATES_QUERY,
      fetchPolicy: "no-cache",
    });
    return data.states;
  },
  async getQuote(stateCode: string, consumptionKwh: number) {
    const { data } = await client.query<QuoteResponse>({
      query: QUOTE_QUERY,
      variables: { stateCode, consumptionKwh },
      fetchPolicy: "no-cache",
    });
    return data.quote;
  },
});
