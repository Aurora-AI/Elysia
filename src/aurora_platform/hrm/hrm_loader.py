import argparse
import yaml
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional


class Rule(BaseModel):
    id: str
    description: str
    when: dict
    then: dict


class RuleSet(BaseModel):
    version: int
    domain: str
    description: Optional[str] = None
    rules: List[Rule] = Field(default_factory=list)


def load_rules(path: str) -> RuleSet:
    data = yaml.safe_load(open(path, "r", encoding="utf-8"))
    return RuleSet(**data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", required=True)
    args = parser.parse_args()
    try:
        rs = load_rules(args.rules)
        print(
            f"OK: {len(rs.rules)} regras carregadas do domínio '{rs.domain}' (v{rs.version}).")
    except ValidationError as ve:
        print("ERRO: Regras inválidas:")
        print(ve.json())


if __name__ == "__main__":
    main()
