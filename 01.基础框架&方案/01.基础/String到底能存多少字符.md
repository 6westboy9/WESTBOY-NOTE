https://mp.weixin.qq.com/s/zLwhN6UfwbEjT6rqtaMPew

### JDK 9 之前

- 底层存储：char 数组，每个字符占 2 个字节（UTF - 16，BMP 字符）。
- 理论最大字符数：Integer.MAX_VALUE（2147483647），受限于 char 数组长度。
- 实际限制：受堆内存大小限制，无法达到理论最大值。
### JDK 9 及之后

- 底层存储：byte 数组，根据编码方式不同，每个字符占 1 或 2 个字节（Latin - 1 或 UTF - 16）。
- Latin - 1 编码：理论最大字符数 Integer.MAX_VALUE（2147483647），每个字符占 1 字节。
- UTF - 16 编码：理论最大字符数 Integer.MAX_VALUE / 2 = 1073741823，每个字符占 2 字节。
- 实际限制：同样受堆内存大小限制，且字符串中的字符如果超出 Latin - 1 范围，会自动使用 UTF - 16 编码，减少可存储的字符数。

