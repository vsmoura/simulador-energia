import { useQuery } from "@apollo/client";
import { useEffect, useRef, useState } from "react";

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

const CalculatorIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon icon-accent">
    <rect x="5" y="3" width="14" height="18" rx="3" stroke="currentColor" strokeWidth="1.6" fill="none" />
    <rect x="8" y="6" width="8" height="3" rx="1" fill="currentColor" />
    <path
      d="M8.5 12.5h1.5M12 12.5h1.5M15.5 12.5h0M8.5 15.5h1.5M12 15.5h1.5M15.5 15.5h0"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
  </svg>
);

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
  const resultRef = useRef<HTMLDivElement | null>(null);

  const handleSubmit = async (values: { stateCode: string; consumptionKwh: number }) => {
    const response = await fetchQuote({
      stateCode: values.stateCode,
      consumptionKwh: values.consumptionKwh,
    });
    if (response.data?.quote) {
      setQuoteData(response.data.quote);
    }
  };
  useEffect(() => {
    if (quoteData && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [quoteData]);

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">clarke</span>
          <span className="brand-accent">energia</span>
        </div>
        <nav className="topbar-actions">
          <a className="ghost" href="https://clarke.com.br/nossas-solucoes/" target="_blank" rel="noreferrer">
            Soluções
          </a>
          <a className="pill" href="https://cliente.clarke.com.br" target="_blank" rel="noreferrer">
            Área do cliente
          </a>
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
            <a className="ghost" href="https://clarke.com.br/" target="_blank" rel="noreferrer">
              Saiba mais
            </a>
          </div>
        </div>

        <section className="panel hero-panel">
          <h2 className="panel-title">
            <CalculatorIcon />
            Simulador de Economia
          </h2>
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

      {quoteData && (
        <div ref={resultRef}>
          <QuoteResult
            key={`${quoteData.stateCode}-${quoteData.consumptionKwh}-${quoteData.baseCost}`}
            data={quoteData}
          />
        </div>
      )}
    </div>
  );
};
