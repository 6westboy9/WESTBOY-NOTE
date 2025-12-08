## 3.1 块级元素

> ([[CSS世界-张鑫旭.pdf#page=28&selection=114,0,156,16&color=red|p.13]])
> “块级元素”对应的英文是 block-level element，常见的块级元素有 `<div>`、`<li>` 和`<table>` 等。需要注意是，<u>“块级元素”和“display 为 block 的元素”不是一个概念</u>。例如，`<li>` 元素默认的 display 值是 list-item，`<table>` 元素默认的 display 值是 table，但是它们均是“块级元素”，因为它们都符合块级元素的基本特征，也就是一个水平流上只能单独显示一个元素，多个块级元素则换行显示。

> ([[CSS世界-张鑫旭.pdf#page=31&selection=120,31,124,1&color=red|p.16]])
> 宽高作用是内在盒子，也就是“容器盒子”


> ([[CSS世界-张鑫旭.pdf#page=33&selection=46,0,54,1&color=red|p.18]])
> 在 CSS 世界中，盒子分“内在盒子”和“外在盒子”，显示也分“内部显示”和“外部显示”，同样地，尺寸也分“内部尺寸”和“外部尺寸”。

> ([[CSS世界-张鑫旭.pdf#page=33&selection=97,0,105,7&color=red|p.18]])
> 在页面中随便扔一个 `<div>` 元素，其尺寸表现就会和这水流一样铺满容器。这就是 block 容器的流特性。

> ([[CSS世界-张鑫旭.pdf#page=33&selection=153,0,164,16&color=red|p.18]])
> 所谓流动性，并不是看上去的宽度 100% 显示这么简单，而是一种 margin/border/padding 和 content 内容区域自动分配水平空间的机制。

```css
.width {  
    width: 100%;  
}  
  
.nav {  
    width: 100px;  
    background-color: #cd0000;  
}  
  
.nav-a {  
    display: block;  
    margin: 0 10px;  
    padding: 9px 10px;  
    border-bottom: 1px solid #b70000;  
    border-top: 1px solid #de3636;  
    color: #fff;  
}  
  
.nav-a:first-child {  
    border-top: 0;  
}  
  
.nav-a:last-child {  
    border-bottom: 0;  
}
```

```html
<h4>无宽度，借助流动性</h4>  
<div class="nav">  
    <a href="" class="nav-a">导航1</a>  
    <a href="" class="nav-a">导航2</a>  
    <a href="" class="nav-a">导航3</a>  
</div>
  
<h4>width:100%</h4>  
<div class="nav">  
    <a href="" class="nav-a width">导航1</a>  
    <a href="" class="nav-a width">导航2</a>  
    <a href="" class="nav-a width">导航3</a>  
</div>
```

![[Pasted image 20251208192401.png|L|300]]

设置了宽度100%

![[Pasted image 20251208192340.png|L|300]]


