import { useQuery } from "@apollo/client";
import { useState } from "react";

import { QuoteForm } from "./QuoteForm";
import { QuoteResult } from "./QuoteResult";
import { QuoteResult as QuoteResultType, StateOption } from "./types";
import { QUOTE_QUERY, STATES_QUERY } from "../../graphql/queries";

interface QuoteResponse {
  quote: QuoteResultType;
}

interface StatesResponse {
  states: StateOption[];
}

export const QuotePage = () => {
  const { data: statesData, loading: statesLoading, error: statesError } = useQuery<StatesResponse>(
    STATES_QUERY,
  );
  const [quoteData, setQuoteData] = useState<QuoteResultType | null>(null);
  const {
    refetch: fetchQuote,
    loading: quoteLoading,
    error: quoteError,
  } = useQuery<QuoteResponse>(QUOTE_QUERY, {
    skip: true,
  });

  const handleSubmit = async (values: { stateCode: string; consumptionKwh: number }) => {
    const response = await fetchQuote({
      stateCode: values.stateCode,
      consumptionKwh: values.consumptionKwh,
    });
    if (response.data?.quote) {
      setQuoteData(response.data.quote);
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <h1>Clarke Energia</h1>
        <p>Simule sua economia com GD e Mercado Livre.</p>
      </header>

      <section className="panel">
        <h2>Simulador de Economia</h2>
        {statesError && <p className="error">Erro ao carregar estados.</p>}
        <QuoteForm
          states={statesData?.states ?? []}
          onSubmit={handleSubmit}
          loading={statesLoading || quoteLoading}
        />
        {quoteError && <p className="error">Erro ao calcular economia.</p>}
      </section>

      {quoteData && <QuoteResult data={quoteData} />}
    </div>
  );
};
