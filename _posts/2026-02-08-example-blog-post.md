---
title: 'Example Blog Post'
date: 2026-02-08
permalink: /posts/2026/02/example-blog-post/
tags:
  - embedded-systems
  - firmware
  - tutorial
---

This is an example blog post. You can write anything here in Markdown!

## How to Write Blog Posts

Blog posts are stored in the `_posts/` directory. The filename format is important:
`YYYY-MM-DD-title.md`

## Formatting

You can use all standard Markdown:

### Code Blocks
```c
// Example STM32 GPIO code
GPIO_TypeDef *gpioa = GPIOA;
gpioa->ODR |= (1 << 5);  // Set pin 5 high
```

### Lists
- Point 1
- Point 2
- Point 3

### Images
![Alt text](/images/your-image.png)

### Links
[Link to Google](https://www.google.com)

## Categories and Tags

Use the front matter (the section between `---` at the top) to organize your posts with tags and categories.
