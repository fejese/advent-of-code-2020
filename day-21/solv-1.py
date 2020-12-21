#!/usr/bin/env python3

from typing import Dict, List, Set, Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

foods: List[Set[str]] = []
ingredients: Set[str] = set()
ingredients_by_allergen: Dict[str, List[Set[str]]] = {}
ingredient_by_allergen: Dict[str, str] = {}
allergen_by_ingredient: Dict[str, str] = {}

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        food, allergens_part = line.strip().strip(")").split(" (contains")
        allergens = allergens_part.strip().split(", ")
        ingrs = set(food.split(" "))
        foods.append(ingrs)
        ingredients.update(ingrs)
        ingredients_by_allergen.update(
            {
                allergen: ingredients_by_allergen.get(allergen, []) + [ingrs]
                for allergen in allergens
            }
        )

print("Foods:", foods)

found_one: bool = True
while ingredients_by_allergen:
    print("Ingredients by allergen:", ingredients_by_allergen)
    print("Ingredient by allergen:", ingredient_by_allergen)
    print("Allergen by ingredient:", allergen_by_ingredient)
    if not found_one:
        raise Exception("Not done but no new matches :(")
    found_one = False
    for allergen, ingredients_lists in ingredients_by_allergen.items():
        for li in ingredients_lists:
            common: Set[str] = set(li)
            for lj in ingredients_lists:
                if li == lj:
                    continue
                common = common.intersection(set(lj))
            if len(common) == 0:
                raise Exception(
                    f"{allergen} is in 2 food without intersection: {li}, {lj}"
                )
            if len(common) > 1:
                continue
            ingredient = common.pop()
            ingredient_by_allergen[allergen] = ingredient
            allergen_by_ingredient[ingredient] = allergen
            ingredients_by_allergen.pop(allergen)
            print(f"Found {ingredient} -> {allergen}")

            for other_ingredients_lists in ingredients_by_allergen.values():
                for other_ingredients_list in other_ingredients_lists:
                    other_ingredients_list -= set([ingredient])
            found_one = True
            break
        if found_one:
            break

print("Ingredients by allergen:", ingredients_by_allergen)
print("Ingredient by allergen:", ingredient_by_allergen)
print("Allergen by ingredient:", allergen_by_ingredient)

matches = sum(
    len([food for food in foods if ingredient in food])
    for ingredient in ingredients - set(allergen_by_ingredient.keys())
)
print("Matches:", matches)
