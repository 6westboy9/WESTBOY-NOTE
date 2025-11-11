# 查询

> [!important] `<where>`标签可以移除第一个多余的`and`或着`or`


# 更新

> [!important] `<set>`标签可以移除多余的`,`，同样`<trim>`标签也可以达到同样的效果

trim标签的几个属性：

* prefix：在trim标签内sql语句加上前缀
* prefixOverride：指定去除多余的前缀内容
* suffix：在trim标签内sql语句加上后缀
* suffixOverrides：指定去除多余的后缀内容

<font color="#f79646">放在后面的逗号（会移除最后一个满足条件的后缀）</font>

```xml
<update id="updateById" parameterType="org.learnhub.mybatis.ds.hikari.entity.UserInfo">
	UPDATE user_info
	<set>
		<if test="username != null">
			username = #{username},
		</if>
		<if test="age != null">
			age = #{age},
		</if>
		<if test="birthDate != null">
			birth_date = #{birthDate},
		</if>
		<if test="createTime != null">
			create_time = #{createTime},
		</if>
		<if test="updateTime != null">
			update_time = #{updateTime},
		</if>
	</set>
	WHERE id = #{id}
</update>
```

等价

```xml
<update id="updateSuccessWithCommaById" parameterType="org.learnhub.mybatis.ds.hikari.entity.UserInfo">
	UPDATE user_info set
	<trim suffixOverrides=",">
		<if test="username != null">
			username = #{username},
		</if>
		<if test="age != null">
			age = #{age},
		</if>
		<if test="birthDate != null">
			birth_date = #{birthDate},
		</if>
		<if test="createTime != null">
			create_time = #{createTime},
		</if>
		<if test="updateTime != null">
			update_time = #{updateTime},
		</if>
	</trim>
	WHERE id = #{id}
</update>
```

最终执行的SQL语句

```sql
UPDATE user_info SET username = ?, age = ?, birth_date = ?, create_time = ?, update_time = ? WHERE id = ?
```

<font color="#f79646">放在前面的逗号（会移除第一个满足条件的前缀）</font>

```xml
<update id="updateWithCommaPrefixById" parameterType="org.learnhub.mybatis.ds.hikari.entity.UserInfo">
	UPDATE user_info
	<set>
		<if test="username != null">
			,username = #{username}
		</if>
		<if test="age != null">
			,age = #{age}
		</if>
		<if test="birthDate != null">
			,birth_date = #{birthDate}
		</if>
		<if test="createTime != null">
			,create_time = #{createTime}
		</if>
		<if test="updateTime != null">
			,update_time = #{updateTime}
		</if>
	</set>
	WHERE id = #{id}
</update>
```

等效

```xml
<update id="updateWithTrimCommaPrefixById" parameterType="org.learnhub.mybatis.ds.hikari.entity.UserInfo">
	UPDATE user_info set
	<trim prefixOverrides=",">
		<if test="username != null">
			,username = #{username}
		</if>
		<if test="age != null">
			,age = #{age}
		</if>
		<if test="birthDate != null">
			,birth_date = #{birthDate}
		</if>
		<if test="createTime != null">
			,create_time = #{createTime}
		</if>
		<if test="updateTime != null">
			,update_time = #{updateTime}
		</if>
	</trim>
	WHERE id = #{id}
</update>
```

最终执行的SQL语句

```sql
UPDATE user_info SET username = ? ,age = ? ,birth_date = ? ,create_time = ? ,update_time = ? WHERE id = ?
```


# 新增


```xml
<insert id="insertSelective" parameterType="org.learnhub.mybatis.ds.hikari.entity.UserInfo" useGeneratedKeys="true" keyProperty="id">
	INSERT INTO user_info
	<trim prefix="(" suffix=")" suffixOverrides=",">
		<if test="username != null">
			username,
		</if>
		<if test="age != null">
			age,
		</if>
		<if test="birthDate != null">
			birth_date,
		</if>
		<if test="createTime != null">
			create_time,
		</if>
		<if test="updateTime != null">
			update_time,
		</if>
	</trim>
	<trim prefix="VALUES (" suffix=")" suffixOverrides=",">
		<if test="username != null">
			#{username},
		</if>
		<if test="age != null">
			#{age},
		</if>
		<if test="birthDate != null">
			#{birthDate},
		</if>
		<if test="createTime != null">
			#{createTime},
		</if>
		<if test="updateTime != null">
			#{updateTime},
		</if>
	</trim>
</insert>
```

最终执行的SQL语句

```sql
INSERT INTO user_info ( username, age, birth_date, create_time, update_time ) VALUES ( ?, ?, ?, ?, ? )
```

# 删除

