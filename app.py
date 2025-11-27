import os
import sys
import json
from utils import load_data, summarize, show_head, describe_numeric, top_values, sum_by, total_revenue, quick_insights

# Optional: import OpenAI if you want LLM integration
try:
    import openai
except ImportError:
    openai = None

def call_llm(api_key, system_prompt, user_prompt):
    if openai is None:
        return "[LLM not available - openai package not installed]"
    openai.api_key = api_key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=system_prompt + '\n\n' + user_prompt,
        max_tokens=400,
        temperature=0.2
    )
    return response.choices[0].text.strip()

def help_text():
    return (
        "Commands:\n"
        "  help              - show this help\n"
        "  head [n]          - show first n rows (default 5)\n"
        "  cols              - list columns\n"
        "  describe          - numeric summary\n"
        "  top <col> [n]     - top values for column\n"
        "  sum <group> <val> - sum value column by group column\n"
        "  total_revenue     - compute total revenue if quantity & unit_price exist\n"
        "  insights          - quick automated insights\n"
        "  ask <natural text> - ask open question (LLM recommended)\n"
        "  exit              - quit\n"
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py path/to/your.csv")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    df = load_data(path)
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    print("Type 'help' for commands.")

    api_key = os.getenv('OPENAI_API_KEY', None)

    while True:
        try:
            cmd = input('> ').strip()
        except KeyboardInterrupt:
            print('\nExiting...')
            break
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0] == 'help':
            print(help_text())
        elif parts[0] == 'head':
            n = int(parts[1]) if len(parts) > 1 else 5
            print(show_head(df, n).to_string(index=False))
        elif parts[0] == 'cols':
            print(', '.join(df.columns))
        elif parts[0] == 'describe':
            print(describe_numeric(df).to_string())
        elif parts[0] == 'top':
            if len(parts) < 2:
                print('Usage: top <column> [n]')
                continue
            col = parts[1]
            n = int(parts[2]) if len(parts) > 2 else 5
            tv = top_values(df, col, n)
            if tv is None:
                print('Column not found or invalid')
            else:
                print(tv.to_string())
        elif parts[0] == 'sum':
            if len(parts) < 3:
                print('Usage: sum <group_col> <value_col>')
                continue
            grp, val = parts[1], parts[2]
            res = sum_by(df, grp, val)
            if res is None:
                print('Columns not found')
            else:
                print(res.to_string())
        elif parts[0] == 'total_revenue':
            tr = total_revenue(df)
            if tr is None:
                print('quantity or unit_price not found')
            else:
                print(f'Total revenue: {tr:.2f}')
        elif parts[0] == 'insights':
            ins = quick_insights(df)
            print(json.dumps(ins, indent=2))
        elif parts[0] == 'ask':
            question = ' '.join(parts[1:])
            if api_key is None:
                print('[No OPENAI_API_KEY found. The ask command can use an LLM for better answers. Set OPENAI_API_KEY to enable.]')
                continue
            context = '\n'.join([', '.join(df.columns), df.head(5).to_csv(index=False)])
            system_prompt = 'You are a helpful data analyst. Use the provided dataset context to answer concisely. If you need code, return only code blocks.'
            user_prompt = f"Dataset context:\n{context}\n\nUser question: {question}"
            print('Asking LLM...')
            answer = call_llm(api_key, system_prompt, user_prompt)
            print(answer)
        elif parts[0] == 'exit':
            break
        else:
            print('Unknown command. Type help for commands.')

if __name__ == '__main__':
    main()
