# from vanna_setup import create_agent

# agent = create_agent()

# examples = [
#     ("How many patients do we have?", "SELECT COUNT(*) FROM patients"),
#     ("List all doctors", "SELECT name FROM doctors"),
#     ("Total revenue", "SELECT SUM(total_amount) FROM invoices"),
#     ("Top patients by spending", "SELECT patient_id, SUM(total_amount) FROM invoices GROUP BY patient_id ORDER BY SUM(total_amount) DESC LIMIT 5"),
#     ("Appointments by status", "SELECT status, COUNT(*) FROM appointments GROUP BY status")
# ]

# for q, sql in examples:
#     agent.agent_memory.add({
#         "question": q,
#         "sql": sql
#     })

# print("✅ Memory seeded successfully!")


# from vanna_setup import create_agent

# agent = create_agent()

# examples = [
#     ("How many patients do we have?", "SELECT COUNT(*) FROM patients"),
#     ("List all doctors", "SELECT name FROM doctors"),
#     ("Total revenue", "SELECT SUM(total_amount) FROM invoices"),
#     ("Top patients by spending", "SELECT patient_id, SUM(total_amount) FROM invoices GROUP BY patient_id ORDER BY SUM(total_amount) DESC LIMIT 5"),
#     ("Appointments by status", "SELECT status, COUNT(*) FROM appointments GROUP BY status")
# ]

# # Use agent tools instead of memory directly
# for q, sql in examples:
#     agent.run_tool(
#         "save_question_tool",   # must match name in vanna_setup.py
#         {
#             "question": q,
#             "sql": sql
#         }
#     )

# print("✅ Memory seeded successfully!")

print("ℹ️ Skipping manual memory seeding (handled dynamically by Vanna during runtime)")