* [Agent 的概念、原理与构建模式 —— 从零打造一个简化版的 Claude Code](https://www.bilibili.com/video/BV1TSg7zuEqR/?spm_id_from=333.337.search-card.all.click&vd_source=401e9151ff5196d99069159680a48dbc)


# ReAct

>Reasoning and Action



## 时许图

```mermaid
sequenceDiagram
    autonumber
    participant U as 用户
    participant A as Agent 主程序
    participant M as 模型
    participant T as 工具（函数）

    U->>A: 写一个贪吃蛇

    loop 重复 n 次
        A->>M: 请求模型
        M-->>A: Thought + Action
        A-->>U: 显示 Thought + Action

        A->>T: 请求 Action 对应的工具
        T-->>A: 工具执行结果
        A-->>U: 显示工具执行结果
    end

    A->>M: 请求模型
    M-->>A: Thought + Final Answer
    A-->>U: Thought + Final Answer
```

## 流程图


```mermaid
flowchart TD
    A[提交任务] --> B[思考]
    B --> C{需要调用工具?}
    C -- 否 --> F[最终答案]

    C -- 是 --> D[行动]
    D --> E[观察]
    E --> B

    T[Thought] -.-> B
    AC[Action] -.-> D
    O[Observation] -.-> E
    FA[Final Answer] -.-> F

    classDef blue fill:#0b78c8,stroke:#0b78c8,color:#ffffff,font-weight:bold;
    classDef green fill:#008000,stroke:#008000,color:#ffffff,font-weight:bold;
    classDef dark fill:#222222,stroke:#222222,color:#ffffff;
    classDef decision fill:#0b78c8,stroke:#0b78c8,color:#ffffff,font-weight:bold;

    class A blue;
    class B,D,E,F green;
    class C decision;
    class T,AC,O,FA dark;

    linkStyle 0,1,2,3,4,5 stroke:#00a2ff,stroke-width:4px;
```

- **提交任务**：接收用户的初始请求。
- **思考（Thought）**：对任务进行分析、推理，判断是否需要借助外部工具来完成。
- **判断是否需要调用工具**：
    - **是**：执行**行动（Action）**，调用对应的工具（如搜索、计算等）。
    - **否**：直接生成**最终答案（Final Answer）**，结束流程。
- **观察（Observation）**：获取工具返回的结果，并将其反馈给**思考**环节，继续迭代推理，直到可以给出最终答案。

# Plan-and-Execute

![[Pasted image 20260323072539.png|L|800]]

## 时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant A as Agent 主程序
    participant P as 🧠 Plan 模型
    participant R as 🧠 Re-Plan 模型
    participant E as 🤖 执行 Agent

    U->>A: 今年奥网男子冠军的家乡是哪里？
    A->>P: 请给出执行计划
    P-->>A: 执行计划如下：...

    rect rgba(144,238,144,0.18)
        loop 重复 n 次
            A->>E: 请执行第一步
            E-->>A: 执行完毕，结果如下……
            A->>R: 请给出一个新的执行计划或者返回最终答案
            R-->>A: 新的执行计划或者最终答案如下：……
        end
    end
```


- **用户提问**：向 Agent 主程序发起问题查询。
- **初始规划**：主程序请求 Plan 模型生成第一步执行计划。
- **迭代执行与重规划**：
    - 主程序将计划步骤交给执行 Agent 执行。
    - 执行完成后，主程序请求 Re-Plan 模型根据当前结果更新后续计划。
    - 循环执行直到问题解决。
- **最终输出**：循环结束后，主程序汇总结果并返回给用户。

# 区别

最核心区别在于：**ReAct 是边想边做，Plan+RePlan 是先规划、再执行、再重规划。**


