import { QuoteResult, StateOption } from "../../domain/quote/types";

export interface QuoteGateway {
  getStates: () => Promise<StateOption[]>;
  getQuote: (stateCode: string, consumptionKwh: number) => Promise<QuoteResult>;
}
