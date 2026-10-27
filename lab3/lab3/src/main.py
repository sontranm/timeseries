import b1_clean_data
import b3_xgboost_model
import b4_advanced
import b5_questions


def main():
    for step in (b1_clean_data, b3_xgboost_model, b4_advanced, b5_questions):
        print(f"\n{'=' * 60}\nRunning {step.__name__}\n{'=' * 60}")
        step.main()
    print("\nLab 3 complete. Figures: docs/figures/ | Tables: data/processed/")


if __name__ == "__main__":
    main()
