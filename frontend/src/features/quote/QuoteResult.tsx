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

const formatSolutionLabel = (value: string) =>
  value === "MERCADO_LIVRE" ? "Mercado Livre" : "Geração Distribuída";

const SolutionCard = ({ solution }: { solution: SolutionQuote }) => (
  <div className="solution-card">
    <div className="solution-header">
      <h3>{formatSolutionLabel(solution.solutionType)}</h3>
      <div>
        <strong>{formatCurrency(solution.bestEconomy)}</strong>
        <span> ({formatPercent(solution.bestEconomyPercent)})</span>
      </div>
    </div>
    <div className="suppliers">
      {solution.suppliers.map((supplier) => (
        <div key={`${supplier.supplierId}-${supplier.solutionType}`} className="supplier-card">
          <div className="supplier-main">
            <img src={supplier.supplierLogoUrl} alt={supplier.supplierName} />
            <div>
              <h4>{supplier.supplierName}</h4>
              <p>Origem: {supplier.supplierOriginState}</p>
            </div>
          </div>
          <div className="supplier-metrics">
            <span>Custo/kWh: {formatCurrency(supplier.costPerKwh)}</span>
            <span>Economia: {formatCurrency(supplier.economy)}</span>
            <span>Economia %: {formatPercent(supplier.economyPercent)}</span>
            <span>Clientes: {supplier.totalCustomers}</span>
            <span>Avaliação: {supplier.averageRating.toFixed(1)}</span>
          </div>
        </div>
      ))}
    </div>
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
        <h2>Resultado para {data.stateCode}</h2>
        <p>
          Consumo: {data.consumptionKwh} kWh | Base: {formatCurrency(data.baseCost)}
        </p>
      </header>

      <div className="solutions">
        {mercadoLivre && <SolutionCard solution={mercadoLivre} />}
        {geracaoDistribuida && <SolutionCard solution={geracaoDistribuida} />}
      </div>
    </section>
  );
};
