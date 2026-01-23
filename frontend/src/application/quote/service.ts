import { QuoteResult, StateOption } from "../../domain/quote/types";
import { QuoteGateway } from "./ports";

export const listStates = (gateway: QuoteGateway): Promise<StateOption[]> => {
  return gateway.getStates();
};

export const calculateQuote = (
  gateway: QuoteGateway,
  stateCode: string,
  consumptionKwh: number,
): Promise<QuoteResult> => {
  return gateway.getQuote(stateCode, consumptionKwh);
};
