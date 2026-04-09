
# C: format string
When `printf` sees a placeholder like `%d` or `%s`, it doesn't actually "know" if you passed a parameter or not. It follows a mechanical process:
1. It sees the `%`.
2. It looks at the **Stack** (the memory area where function arguments are stored).
3. It grabs whatever data happens to be sitting in the next "argument slot" and treats it as the value for that placeholder.



# The Golden Rule 
`printf`
To avoid the security bugs we discussed, a programmer should **never** do this:
`printf(user_input);` ❌

They should **always** do this:
`printf("%s", user_input);` ✅

* **`gets(buffer)`**: This function is "blind." It reads characters from your keyboard until you hit Enter. It doesn't know how big `buffer` is. If your buffer is 10 bytes and you type 50, it just keeps writing into the next 40 bytes of memory.
* **`scanf("%s", buffer)`**: This is just as dangerous. The `%s` format tells it to "read a string until you see a space." Like `gets`, it doesn't check the size. 

> **The Safe Alternative:** Professionals use `fgets(buffer, sizeof(buffer), stdin)`. The `sizeof` part acts as a "security guard" that stops the writing as soon as the limit is reached.
