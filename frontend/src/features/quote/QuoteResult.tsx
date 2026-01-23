import { QuoteResult as QuoteResultType, SolutionQuote } from "./types";

interface QuoteResultProps {
  data: QuoteResultType;
}

const formatCurrency = (value: number) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);

const formatPercent = (value: number) => `${(value * 100).toFixed(2)}%`;

const formatRank = (index: number) => `${index + 1}º`;

const formatSolutionLabel = (value: string) =>
  value === "MERCADO_LIVRE" ? "Mercado Livre" : "Geração Distribuída";

const CurrencyIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M5.5 6.5h9a3.5 3.5 0 0 1 0 7h-9m0-7v11m0-11h10a3.5 3.5 0 0 1 0 7h-10"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
  </svg>
);

const TrendIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M4 16l6-6 4 4 6-6"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path d="M16 6h4v4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
  </svg>
);

const UsersIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M8.5 13a3 3 0 1 0-0.001-6.001A3 3 0 0 0 8.5 13Zm7 0a3 3 0 1 0-0.001-6.001A3 3 0 0 0 15.5 13Z"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
    />
    <path
      d="M3.5 20a5 5 0 0 1 10 0m1-0a5 5 0 0 1 7 0"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
  </svg>
);

const StarIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M12 4.5 14.3 9l4.9.7-3.6 3.5.8 4.9L12 15.8 7.6 18l.8-4.9-3.6-3.5 4.9-.7L12 4.5Z"
      fill="currentColor"
    />
  </svg>
);

const SolutionCard = ({ solution }: { solution: SolutionQuote }) => (
  <div className="solution-card">
    <div className="solution-header">
      <h3>{formatSolutionLabel(solution.solutionType)}</h3>
      <div>
        <strong>{formatCurrency(solution.bestEconomy)}</strong>
        <span> ({formatPercent(solution.bestEconomyPercent)})</span>
      </div>
    </div>
    <ol className="supplier-list">
      {solution.suppliers.map((supplier, index) => (
        <li key={`${supplier.supplierId}-${supplier.solutionType}`} className="supplier-item">
          <details>
            <summary>
              <span className="rank">{formatRank(index)}</span>
              <img src={supplier.supplierLogoUrl} alt={supplier.supplierName} />
              <span className="supplier-name">{supplier.supplierName}</span>
              <span className="supplier-rating">
                <StarIcon />
                {supplier.averageRating.toFixed(1)}
              </span>
              <span className="supplier-economy">
                {formatPercent(supplier.economyPercent)}
              </span>
            </summary>
            <div className="supplier-details">
              <div className="supplier-metrics">
                <span>
                  <CurrencyIcon />
                  Custo/kWh: {formatCurrency(supplier.costPerKwh)}
                </span>
                <span>
                  <TrendIcon />
                  Economia: {formatCurrency(supplier.economy)}
                </span>
                <span>
                  <CurrencyIcon />
                  Custo final: {formatCurrency(supplier.costTotal)}
                </span>
                <span>
                  <UsersIcon />
                  Clientes: {supplier.totalCustomers}
                </span>
              </div>
            </div>
          </details>
        </li>
      ))}
    </ol>
  </div>
);

const solutionByType = (solutions: SolutionQuote[], type: string) =>
  solutions.find((solution) => solution.solutionType === type);

export const QuoteResult = ({ data }: QuoteResultProps) => {
  const mercadoLivre = solutionByType(data.solutions, "MERCADO_LIVRE");
  const geracaoDistribuida = solutionByType(data.solutions, "GD");

  return (
    <section className="quote-result">
      <header>
        <h2>Análise Energética para {data.stateName}</h2>
        <p>
          Atualmente, com o consumo de <strong>{data.consumptionKwh} kWh</strong> na tarifa
          convencional da distribuidora estadual, seu custo mensal é de{" "}
          <strong>{formatCurrency(data.baseCost)}</strong>.
        </p>
      </header>

      <div className="solutions">
        {mercadoLivre && <SolutionCard solution={mercadoLivre} />}
        {geracaoDistribuida && <SolutionCard solution={geracaoDistribuida} />}
      </div>
    </section>
  );
};
