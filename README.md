# Swirly 🌀

**Swirly** is a CLI-based interactive trainer for learning ~~pandas~~ _different python packages_, inspired by the great R package [Swirl](https://swirlstats.com/). (I initially thought of **Swirly** to learn `pandas` 😉).

The idea is that you can learn ~~Pandas~~ whatever package you choose, right there, interacting with it.

Swirly offers you different lessons to choose from. Lessons can have as many (or few) questions as the lesson designer wants, and the response to each question is tested for correctness.

Moreover, you can add, share, modify and redistribute any lesson!

# Install

There are two possible ways to install and run **Swirly**: in a virtual environment, or as a stand-alone app with `pipx`. The Instructions below are for a Linux system:

## 🚀 Install in a virtual environment

```bash
git clone https://github.com/PavoDive/swirly.git
cd swirly
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
swirly
```

## 🪄 Alternative: install globally with pipx

```bash
pipx install git+https://github.com/PavoDive/swirly.git swirly
```

# How to use Swirly

When you enter **Swirly**, you'll be asked to choose from a set of lessons (or you'll be taken to resume your previous one). Within each lesson you'll be asked a set of questions, and you're expected to provide the right answer in order to advance to the next question. The correctness of answers is validated against the result, so that legit variations in syntax are accepted as valid answers.

Once in a **Swirly** lesson, there are some commands that may come useful:

## 💡 Commands

- `next` — Skip to next question. This will advance you to the next question, providing the expected answer.
- `reveal` — Show correct answer (does not advance).
- `play` — Drop into free Python mode. The objects created during the lesson will be accessible, so the user can experiment and explore freely with them.
- `info` — Show this help.
- `bye` — Exit **Swirly**, saving the current lesson's advance.

Upon completing a lesson, the lesson's advance will be deleted, so if you want to redo that lesson, **Swirly** will start from the very beggining.

At any point during a lesson, the student can use any help command, that will not be taken as an answer: Commands such as `help(print)`, `dir()` or `dir(df)`.

## 📚 Lessons

Lessons are powered by YAML files in `swirly/lessons/`.

This means that you can modify or develop your own lessons!

Any **Swirly** lesson has the following structure: a metadata block, and a `steps` block.

Lessons live within the `lessons` directory of **Swirly**, so adding a new lesson is as simple as just copying (or creating) a valid `yaml` file to it.

### Lesson's metadata

Every lesson should have the following fields as metadata:

- A **title**.
- A **slug**.
- The **author** of the lesson.
- A **preamble**. This part is used to preload any objects that are needed in the lesson: import of packages, object creation and the like. It is run by **Swirly** every time the user starts or reloads the lesson.
- A **description** of the lesson.

### Lesson's steps

The `steps` are the actual questions of the lesson. A step has the following fields:

- [Required] A **prompt**, the text asked to the user. Ideally it provides hints to the names of objects required to complete the task.
- [Required] An **answer**. This is the code that will produce the expected result. As explained before, **Swirly** does not compare the user's input to the expected answer, but the _results_ of the user input against the _results_ of the expected answer.
- [Optional] A **setup**, this is the expression that needs to be exectued silently by **Swirly** to produce the expected result. This is particularly used when an assignment is required, see the example below.
. [Optional] A **var**: When the step involves assigning a vale (for instance `s = pd.Series(...)`), set `var` to the variable name (`s` in this case). This tells **Swirly** to evaluate the users's input using `exec()`, then fetch `env.vars['s']` and compare it to the expected result. It must match the name assigned in the user's code and in the `setup` part of the step.

> If `var` is not provided, **Swirly** assumes the answer is an expression and uses `eval()` (instead of `exec()`) to capture and compare results.

This excerpt from the lesson on the basics of series (`series_basics.yaml`) shows how this fields are used in some steps:

```yaml
steps:
- prompt: "Import pandas using the alias 'pd'."
  answer: pd
  setup: import pandas as pd
  var: pd

- prompt: "Create a Series 's' with values [10, 20, 30]."
  answer: pd.Series([10, 20, 30])
  setup: s = pd.Series([10, 20, 30])
  var: s
```

# Contributing

**Swirly** is a work in progress, licensed under the GPL-v3, so you have the four freedoms:  [the freedom to run; study and change; redistribute; and modify (hopefully improve!) it](https://www.gnu.org/philosophy/free-sw.html).

Please submit an issue if you find any bug, and please share your lessons! All Contributions welcome!
