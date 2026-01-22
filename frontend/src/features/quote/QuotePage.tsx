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
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">clarke</span>
          <span className="brand-accent">energia</span>
        </div>
        <nav className="topbar-actions">
          <button className="ghost" type="button">
            Soluções
          </button>
          <button className="ghost" type="button">
            Conteúdo
          </button>
          <button className="pill" type="button">
            Área do cliente
          </button>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-content">
          <span className="eyebrow">Mercado Livre de Energia</span>
          <h1>
            Sua empresa <span className="accent">eficiente</span> no Mercado Livre de Energia
          </h1>
          <p>
            A Clarke Energia conecta sua empresa aos melhores fornecedores e ajuda a transformar
            custo em economia com tecnologia e transparência.
          </p>
          <div className="hero-cta">
            <button className="ghost" type="button">
              Saiba mais
            </button>
            <button className="primary" type="button">
              Simular economia
            </button>
          </div>
        </div>

        <section className="panel hero-panel">
          <h2>Simulador de Economia</h2>
          <p>
            Calcule quanto você pode economizar na conta de luz.
          </p>
          {statesError && <p className="error">Erro ao carregar estados.</p>}
          <QuoteForm
            states={statesData?.states ?? []}
            onSubmit={handleSubmit}
            loading={statesLoading || quoteLoading}
          />
          {quoteError && <p className="error">Erro ao calcular economia.</p>}
        </section>
      </section>

      {quoteData && <QuoteResult data={quoteData} />}
    </div>
  );
};
