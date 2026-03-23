#### Option A: The Internal Pipe (Your First Example)
`awk 'BEGIN { FS = ":" } { print $1 | "sort" }' target.file`
* **How it works:** AWK starts the `sort` process itself. It "talks" to `sort` directly.
* **Pro:** You can do complex things, like sending `$1` to `sort` and `$2` to a different command entirely, all within one AWK script.

#### Option B: The Shell Pipe (The "Classic" Way)
`awk -F: '{ print $1 }' target.file | sort`
* **How it works:** AWK does its job (printing the first column), finishes, and then the **Shell** (Bash/Zsh) grabs that output and hands it to `sort`.
* **Pro:** It is often easier to read and slightly faster for simple tasks.
* **Note on `-F:`:** This is just a shortcut for `BEGIN { FS = ":" }`.

### 3. Why the Manual looks different
When you see `BEGIN { FS = ":" } ...` in a book, they are often assuming you are writing an **AWK Script File** (e.g., `myscript.awk`).

If you put that code into a file called `myscript.awk`, you would run it like this:
`awk -f myscript.awk target.file`

