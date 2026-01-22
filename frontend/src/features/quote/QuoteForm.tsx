import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { StateOption } from "./types";

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

export const QuoteForm = ({ states, onSubmit, loading }: QuoteFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { stateCode: "", consumptionKwh: 30000 },
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
        Estado (UF)
        <select {...register("stateCode")} disabled={loading}>
          <option value="">Selecione</option>
          {stateOptions}
        </select>
        {errors.stateCode && <span className="error">{errors.stateCode.message}</span>}
      </label>

      <label>
        Consumo mensal (kWh)
        <input
          type="number"
          step="1"
          min="1"
          {...register("consumptionKwh", { valueAsNumber: true })}
          disabled={loading}
        />
        {errors.consumptionKwh && (
          <span className="error">{errors.consumptionKwh.message}</span>
        )}
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Calculando..." : "Calcular economia"}
      </button>
    </form>
  );
};
