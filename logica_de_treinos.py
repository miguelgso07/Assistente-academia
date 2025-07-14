
import pandas as pd

class GeradorDosTreinos:
    """Gera planos de treino semanais com base nos parâmetros do usuário."""
    def __init__(self, df_exercicios):
        if df_exercicios is None or df_exercicios.empty:
            raise ValueError("O DataFrame de exercícios não pode ser nulo ou vazio.")
        self.df = df_exercicios

    def _get_random_exercises(self, group, num, ex_type, exclude_names, high_demand):
        """Seleciona exercícios aleatórios de forma segura."""
        available = self.df[(self.df["Grupo"] == group) & (~self.df["Nome"].isin(exclude_names))]
        
        if ex_type:
            typed_available = available[available["Tipo"] == ex_type]
            if not typed_available.empty:
                available = typed_available

        if available.empty:
            return []

        # Prioriza alta demanda se solicitado
        if high_demand:
            high_demand_options = available[available["DemandaEnergetica"] == "Alta"]
            if not high_demand_options.empty:
                return high_demand_options.sample(min(len(high_demand_options), num)).to_dict('records')
        
        return available.sample(min(len(available), num)).to_dict('records')

    def _build_day_exercises(self, structure, high_demand):
        """Constrói a lista de exercícios para um dia, evitando repetição de código."""
        exercises = []
        picked_names = set()
        
        for group, num, ex_type in structure:
            new_ex = self._get_random_exercises(group, num, ex_type, picked_names, high_demand)
            exercises.extend(new_ex)
            picked_names.update(ex['Nome'] for ex in new_ex)
            
        return exercises

    def generate_weekly_plan(self, nivel, imc_classificacao, aerobic_time):
        """Gera um plano de 5 dias com base no nível do usuário."""
        plan = {}
        high_demand = "Obesidade" in imc_classificacao or "Sobrepeso" in imc_classificacao
        aerobic_entry = {"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}
        rest_entry = {"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}

        # Estruturas de treino para cada nível
        if nivel == "Básico":
            day1_struct = [("Peito", 2, "Composto"), ("Peito", 1, "Isolado"), ("Tríceps", 2, None), ("Abdômen", 1, None)]
            day2_struct = [("Costas", 3, "Composto"), ("Bíceps", 2, None)]
            day3_struct = [("Pernas", 3, "Composto"), ("Pernas", 1, "Isolado"), ("Ombros", 2, "Composto")]
            
            plan["Dia 1"] = self._build_day_exercises(day1_struct, high_demand) + [aerobic_entry]
            plan["Dia 2"] = self._build_day_exercises(day2_struct, high_demand) + [aerobic_entry]
            plan["Dia 3"] = self._build_day_exercises(day3_struct, high_demand) + [aerobic_entry]
            plan["Dia 4"] = [rest_entry]
            plan["Dia 5"] = [rest_entry]

        elif nivel == "Intermediário":
            # PPL + Upper/Lower
            day1_struct = [("Peito", 2, "Composto"), ("Ombros", 1, "Composto"), ("Tríceps", 2, None)] # Push
            day2_struct = [("Costas", 3, "Composto"), ("Bíceps", 2, None)] # Pull
            day3_struct = [("Pernas", 3, "Composto"), ("Pernas", 1, "Isolado"), ("Abdômen", 2, None)] # Legs
            day4_struct = [("Peito", 1, "Composto"), ("Costas", 1, "Composto"), ("Ombros", 1, "Composto"), ("Bíceps", 1, None), ("Tríceps", 1, None)] # Upper
            day5_struct = [("Pernas", 2, "Composto"), ("Abdômen", 2, None)] # Lower

            plan["Dia 1"] = self._build_day_exercises(day1_struct, high_demand) + [aerobic_entry]
            plan["Dia 2"] = self._build_day_exercises(day2_struct, high_demand) + [aerobic_entry]
            plan["Dia 3"] = self._build_day_exercises(day3_struct, high_demand) + [aerobic_entry]
            plan["Dia 4"] = self._build_day_exercises(day4_struct, high_demand) + [aerobic_entry]
            plan["Dia 5"] = self._build_day_exercises(day5_struct, high_demand) + [aerobic_entry]

        elif nivel == "Avançado":
            # Upper/Lower
            day1_struct = [("Peito", 2, "Composto"), ("Costas", 2, "Composto"), ("Ombros", 1, "Composto"), ("Bíceps", 1, None), ("Tríceps", 1, None)] # Upper
            day2_struct = [("Pernas", 3, "Composto"), ("Pernas", 2, "Isolado"), ("Abdômen", 2, None)] # Lower
            day3_struct = [("Peito", 1, "Composto"), ("Peito", 1, "Isolado"), ("Costas", 1, "Composto"), ("Costas", 1, "Isolado"), ("Ombros", 1, "Isolado"), ("Bíceps", 1, None), ("Tríceps", 1, None)] # Upper Var
            day4_struct = [("Pernas", 2, "Composto"), ("Pernas", 1, "Isolado"), ("Abdômen", 1, None)] # Lower Var

            plan["Dia 1"] = self._build_day_exercises(day1_struct, high_demand) + [aerobic_entry]
            plan["Dia 2"] = self._build_day_exercises(day2_struct, high_demand) + [aerobic_entry]
            plan["Dia 3"] = self._build_day_exercises(day3_struct, high_demand) + [aerobic_entry]
            plan["Dia 4"] = self._build_day_exercises(day4_struct, high_demand) + [aerobic_entry]
            plan["Dia 5"] = [rest_entry]

        return plan