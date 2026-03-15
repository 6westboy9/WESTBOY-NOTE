

```css
a {
   width: 200px
   margin-right: 50px
   margin-top: 50px
}
```


![[Pasted image 20260308210404.png|L|600]]


a标签说一个行内元素，生成的是一个行内盒子，行内盒子不会独占一行，和文字在同一行内排列，**设置的宽度和高度会被忽略，水平方向的margin和padding会推开周围内容，但垂直方向的不会**。

可以通过display属性来改变元素的布局行为，把a标签的display属性改为block

```css
a {
	display: block
}
```







