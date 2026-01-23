import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { StateOption } from "../../domain/quote/types";

const schema = z.object({
  stateCode: z.string().min(2, "Selecione um estado"),
  consumptionKwh: z
    .number({ invalid_type_error: "Informe um consumo válido" })
    .positive("O consumo deve ser maior que zero"),
});

type FormValues = z.infer<typeof schema>;

interface QuoteFormProps {
  states: StateOption[];
  onSubmit: (values: FormValues) => void;
  loading?: boolean;
}

const LocationIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M12 3.5c-3.3 0-6 2.7-6 6 0 4.7 6 10 6 10s6-5.3 6-10c0-3.3-2.7-6-6-6Z"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
    />
    <circle cx="12" cy="9.5" r="2.5" fill="currentColor" />
  </svg>
);

const EnergyIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className="icon">
    <path
      d="M13 2L6 13h5l-1 9 8-12h-5l1-8Z"
      fill="currentColor"
    />
  </svg>
);

export const QuoteForm = ({ states, onSubmit, loading }: QuoteFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { stateCode: "" },
  });

  const stateOptions = useMemo(
    () =>
      states.map((state) => (
        <option key={state.code} value={state.code}>
          {state.code} - {state.name}
        </option>
      )),
    [states],
  );

  return (
    <form className="quote-form" onSubmit={handleSubmit(onSubmit)}>
      <label>
        <span className="label">
          <LocationIcon />
          Estado (UF)
        </span>
        <select {...register("stateCode")} disabled={loading}>
          <option value="">Selecione</option>
          {stateOptions}
        </select>
        {errors.stateCode && <span className="error">{errors.stateCode.message}</span>}
      </label>

      <label>
        <span className="label">
          <EnergyIcon />
          Consumo mensal (kWh)
        </span>
        <input
          type="number"
          step="1"
          min="1"
          placeholder="15000"
          {...register("consumptionKwh", { valueAsNumber: true })}
          disabled={loading}
        />
        {errors.consumptionKwh && (
          <span className="error">{errors.consumptionKwh.message}</span>
        )}
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Calculando..." : "Calcular"}
      </button>
    </form>
  );
};
