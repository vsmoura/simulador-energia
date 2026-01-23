export type SolutionType = "GD" | "MERCADO_LIVRE";

export interface StateOption {
  code: string;
  name: string;
  baseTariffPerKwh: number;
}

export interface SupplierQuote {
  supplierId: number;
  supplierName: string;
  supplierLogoUrl: string;
  supplierOriginState: string;
  totalCustomers: number;
  averageRating: number;
  solutionType: SolutionType;
  costPerKwh: number;
  costTotal: number;
  economy: number;
  economyPercent: number;
}

export interface SolutionQuote {
  solutionType: SolutionType;
  bestEconomy: number;
  bestEconomyPercent: number;
  suppliers: SupplierQuote[];
}

export interface QuoteResult {
  stateCode: string;
  stateName: string;
  baseTariffPerKwh: number;
  consumptionKwh: number;
  baseCost: number;
  solutions: SolutionQuote[];
}
