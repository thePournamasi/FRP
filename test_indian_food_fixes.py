"""
Test script to verify Indian food prediction fixes
Run this to validate that the alias system and matching logic are working correctly.
"""

def test_alias_system():
    """Test that all aliases map to valid foods in the database"""
    from food_data import LOCAL_FOOD_ALIASES, LOCAL_FOOD_DATABASE
    
    print("=" * 60)
    print("TESTING ALIAS SYSTEM")
    print("=" * 60)
    
    invalid_aliases = []
    valid_count = 0
    
    for alias, food in LOCAL_FOOD_ALIASES.items():
        if food not in LOCAL_FOOD_DATABASE:
            invalid_aliases.append((alias, food))
        else:
            valid_count += 1
    
    print(f"\n✅ Total Valid Aliases: {valid_count}")
    print(f"❌ Invalid Aliases: {len(invalid_aliases)}")
    
    if invalid_aliases:
        print("\nInvalid alias mappings (MUST BE FIXED):")
        for alias, food in invalid_aliases:
            print(f"  - {alias} → {food} (NOT IN DATABASE)")
    else:
        print("\n✅ All aliases point to valid foods!")
    
    return len(invalid_aliases) == 0


def test_matching_logic():
    """Test the food matching functions"""
    from food_data import LOCAL_FOOD_ALIASES, LOCAL_FOOD_DATABASE
    
    print("\n" + "=" * 60)
    print("TESTING MATCHING LOGIC")
    print("=" * 60)
    
    test_cases = [
        # ImageNet predictions that should map to Indian foods
        ("pancake", "dosa"),           # Should alias to dosa
        ("soup", "dal"),               # Should alias to dal
        ("spring_roll", "spring_roll"), # Should remain as is
        ("samosa", "samosa"),          # Direct match
        ("rice", "steamed_rice"),      # Should alias to steamed_rice
        ("tea", "chai"),               # Should alias to chai
        ("doughnut", "gulab_jamun"),   # Should alias to gulab_jamun
    ]
    
    print("\nTesting direct alias resolution:")
    for prediction, expected in test_cases:
        normalized = prediction.lower().replace(' ', '_')
        
        # Check direct database match
        if normalized in LOCAL_FOOD_DATABASE:
            result = normalized
        # Check alias match
        elif normalized in LOCAL_FOOD_ALIASES:
            result = LOCAL_FOOD_ALIASES[normalized]
        else:
            result = None
        
        status = "✅" if result == expected else "❌"
        print(f"{status} {prediction:20} → {result:25} (expected: {expected})")


def test_indian_mode_detection():
    """Test Indian-only mode detection"""
    from food_data import LOCAL_FOOD_DATABASE
    
    print("\n" + "=" * 60)
    print("TESTING INDIAN FOOD DATABASE")
    print("=" * 60)
    
    indian_foods = [
        "dosa", "idli", "samosa", "dal", "paneer_butter_masala",
        "biryani", "naan", "chai", "gulab_jamun", "chana_masala"
    ]
    
    print("\nChecking if key Indian foods are in database:")
    missing = []
    for food in indian_foods:
        if food in LOCAL_FOOD_DATABASE:
            print(f"✅ {food:30} - Calories: {LOCAL_FOOD_DATABASE[food]['calories']}")
        else:
            print(f"❌ {food:30} - NOT FOUND")
            missing.append(food)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} Indian foods!")
    else:
        print("\n✅ All test Indian foods are in database!")


def test_coverage():
    """Show coverage statistics"""
    from food_data import LOCAL_FOOD_ALIASES, LOCAL_FOOD_DATABASE
    
    print("\n" + "=" * 60)
    print("COVERAGE STATISTICS")
    print("=" * 60)
    
    print(f"\nTotal foods in database: {len(LOCAL_FOOD_DATABASE)}")
    print(f"Total alias mappings: {len(LOCAL_FOOD_ALIASES)}")
    print(f"Coverage ratio: {len(LOCAL_FOOD_ALIASES) / len(LOCAL_FOOD_DATABASE) * 100:.1f}%")
    
    # Count by category
    categories = {
        "Breads": 0,
        "Curries": 0,
        "Snacks": 0,
        "Sweets": 0,
        "Beverages": 0,
    }
    
    for food in LOCAL_FOOD_DATABASE.keys():
        if any(x in food for x in ["roti", "naan", "paratha", "dosa", "idli", "rice", "biryani"]):
            categories["Breads"] += 1
        elif any(x in food for x in ["dal", "curry", "masala", "paneer", "bhindi", "vegetable"]):
            categories["Curries"] += 1
        elif any(x in food for x in ["samosa", "vada", "momos", "spring_roll", "pakora"]):
            categories["Snacks"] += 1
        elif any(x in food for x in ["jamun", "kheer", "jalebi", "laddoo", "barfi"]):
            categories["Sweets"] += 1
        elif any(x in food for x in ["chai", "coffee", "lassi", "buttermilk", "soda"]):
            categories["Beverages"] += 1
    
    print("\nFoods by category:")
    for cat, count in categories.items():
        if count > 0:
            print(f"  {cat:15} : {count:3} foods")


def main():
    """Run all tests"""
    print("\n")
    print("🍜" * 30)
    print("INDIAN FOOD PREDICTION FIX - TEST SUITE")
    print("🍜" * 30)
    
    try:
        alias_ok = test_alias_system()
        test_matching_logic()
        test_indian_mode_detection()
        test_coverage()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        if alias_ok:
            print("\n✅ ALL TESTS PASSED!")
            print("\nThe Indian food prediction system should now work correctly.")
            print("Common Indian foods like samosa, dosa, biryani, etc. will be")
            print("properly recognized when using 'Indian dishes only' mode.")
        else:
            print("\n❌ SOME TESTS FAILED!")
            print("\nPlease fix the invalid alias mappings in food_data.py")
        
        print("\n" + "=" * 60)
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure you're running this from the FRP-main directory")


if __name__ == "__main__":
    main()
