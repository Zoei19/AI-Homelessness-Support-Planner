# How to Run the Evaluation Suite

1. Load each scenario (scenario1.json, scenario2.json, scenario3.json).
2. Pass each user_input into the agent conversation entrypoint.
3. Confirm transitions:
   - A1 → A2 → A3 → A4
4. Verify:
   - Memory bank stores each stage
   - Tools are called (uk_services_lookup, postcode_geo, html_pdf_generator)
   - Output matches patterns in expected_outputs.md
