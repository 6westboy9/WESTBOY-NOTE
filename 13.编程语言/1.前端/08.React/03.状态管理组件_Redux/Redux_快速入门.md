# Redux 是什么？

*Redux 是一个“全局状态仓库 + 严格更新规则”的管理工具。*

你可以把它理解成：

> 👉 整个应用只有一个“总账本（store）”，  
> 👉 所有数据修改必须走“申请流程（action）”，  
> 👉 由“专门的处理员（reducer）”按规则修改。


# 为什么需要 Redux？

*场景：组件多了之后会发生什么？*

你做前端（比如 Vue3 / React），一定遇到过这种情况：

- A 组件修改数据
- B 组件也依赖这个数据
- C 组件嵌套很深
- D 组件又要通知 A 更新

然后你会看到：

- props 一层层传
- event 一层层往上抛
- 数据来源混乱
- 状态同步出 bug

这就是典型的：

> ❌ “状态分散、数据混乱、难以维护”

# Redux 解决的核心问题

Redux 真正重要的不是库本身，而是：

>🔥 “可预测的数据流”

数据流永远是**单向**的：

```
UI -> dispatch -> reducer -> store -> UI
```

详细版本：

```
UI 触发操作
   ↓
dispatch(action)
   ↓
reducer(state, action)
   ↓
生成 newState
   ↓
store 更新
   ↓
通知所有订阅者
   ↓
UI 重新渲染
```

而不是：

```
A 改 B
B 通知 C
C 又改 A
```

这种“数据乱飞”是大型项目的灾难。


# Redux Toolkit 又是什么？与 Redux 区别？

*一句话区别*

> **Redux = 底层核心库（原始 API）**  
> **Redux Toolkit = 官方封装的最佳实践集合（更现代、更简洁）**

Redux Toolkit 是官方推荐的写法。

|对比点|Redux|Redux Toolkit|
|---|---|---|
|写法复杂度|高|低|
|是否需要手动写 action|是|不需要|
|是否需要手动写 reducer switch|是|不需要|
|是否需要手动配置 middleware|是|自动配置|
|是否默认支持不可变更新|需要自己写|内置 Immer|
|官方推荐程度|旧写法|⭐⭐⭐ 官方推荐|

# redux-saga

你想弄明白「为什么非要用 redux-saga」以及「只靠原生 Redux 能不能搞定所有需求」，核心答案是：**只靠 Redux 能实现基础功能，但处理复杂异步逻辑会非常痛苦，redux-saga 是为了解决 Redux 原生处理异步的痛点而生的**。

## 1.先明确：Redux 本身的定位

Redux 是一个**状态管理库**，核心职责只有 3 件事：

1. 用 `store` 存储全局状态；
2. 用 `reducer` 纯函数同步更新状态；
3. 用 `action` 描述状态变更的意图。

Redux **原生不支持异步** —— 它的设计原则是「reducer 必须是纯函数」（不能有网络请求、定时器、副作用），所以原生 Redux 只能处理**同步的状态更新**。

## 2.只靠 Redux（不加中间件）会遇到什么问题？

如果完全不用 redux-saga/thunk 等中间件，你想在 Redux 中处理异步（比如接口请求），只能这么做：

```js
// 组件中直接写异步逻辑（反例！）
function UserComponent() {
  const dispatch = useDispatch();
  
  const fetchUser = async () => {
    // 1. 手动发 "加载中" action
    dispatch({ type: 'FETCH_USER_LOADING' });
    try {
      // 2. 手动调接口
      const res = await fetch('/api/user');
      // 3. 手动发 "成功" action
      dispatch({ type: 'FETCH_USER_SUCCESS', payload: res });
    } catch (e) {
      // 4. 手动发 "失败" action
      dispatch({ type: 'FETCH_USER_FAILURE', payload: e });
    }
  };

  return <button onClick={fetchUser}>获取用户</button>;
}
```

这种写法的致命问题：

1. **异步逻辑和组件紧耦合**：每个组件都要重复写「加载中 / 成功 / 失败」的逻辑，代码冗余、难维护；
2. **无法控制复杂流程**：比如「取消重复请求」「轮询接口」「多个请求串行 / 并行」「请求失败重试」，在组件里写会极其复杂；
3. **难测试**：异步逻辑和 UI 组件混在一起，单元测试要模拟 DOM、网络请求，成本极高；
4. **违背单一职责**：组件本该只负责「渲染 UI + 触发交互」，却要承担异步逻辑、错误处理等额外职责。

简单说：**只靠 Redux 能跑通，但代码会乱成一团，尤其在中大型项目中完全不可维护**。

## 3.为什么需要 redux-saga？它解决了什么核心痛点？

redux-saga 是 Redux 的**异步中间件**，核心是把「异步逻辑」从组件和 reducer 中抽离出来，专门交给 saga 管理，解决了以下关键问题：

### 异步逻辑和组件解耦

所有异步代码集中在 saga 文件中，组件只需要「发 action」，不用关心后续逻辑：

```js
// 组件（只负责发 action）
<button onClick={() => dispatch({ type: 'FETCH_USER', payload: 1 })}>获取用户</button>

// saga（专门处理异步）
function* fetchUserSaga(action) {
  yield put({ type: 'FETCH_USER_LOADING' });
  try {
    const res = yield call(fetchUserApi, action.payload);
    yield put({ type: 'FETCH_USER_SUCCESS', payload: res });
  } catch (e) {
    yield put({ type: 'FETCH_USER_FAILURE', payload: e });
  }
}
```

### 强大的复杂流程控制能力

这是 redux-saga 最核心的优势，原生 Redux + 组件根本做不到（或极难做到）：

- **取消重复请求**：`takeLatest` 自动取消前一次未完成的请求（比如用户快速点击按钮）；
- **请求防抖 / 节流**：`takeLeading`/`delay` 实现防抖，避免频繁请求；
- **多请求协调**：`all` 并行请求、`race` 竞态请求（谁先返回用谁）；
- **轮询 / 定时任务**：`while(true) + delay` 实现接口轮询；
- **请求重试**：`retry` 或手动循环实现失败重试；
- **监听全局 action**：`take` 监听任意 action，实现跨组件的流程联动。

#### 1.取消重复请求

**场景**：用户快速点击 “获取数据” 按钮，取消前一次未完成的请求，只保留最后一次请求（避免接口返回顺序混乱）。

```js
import { takeLatest, call, put } from 'redux-saga/effects';

// 模拟接口请求（带延迟）
const fetchDataApi = (id) => {
  return new Promise((resolve) => {
    setTimeout(() => resolve({ id }), 1000); // 模拟1秒请求耗时
  });
};

// 处理单个请求的 saga
function* fetchDataSaga(action) {
  try {
    const data = yield call(fetchDataApi, action.payload);
    yield put({ type: 'FETCH_DATA_SUCCESS', payload: data });
  } catch (e) {
    yield put({ type: 'FETCH_DATA_FAILURE', payload: e.message });
  }
}

// 监听 action，自动取消重复请求
export function* watchFetchData() {
  // takeLatest：监听 'FETCH_DATA' action，有新请求时取消旧请求
  yield takeLatest('FETCH_DATA', fetchDataSaga);
}
```

**效果**：用户 1 秒内点击 3 次按钮，只会执行最后一次请求，前 2 次未完成的请求会被取消。

#### 2.只执行第一次请求（takeLeading）

**场景**：防止用户重复提交表单（比如支付按钮），点击一次后锁定，直到请求完成才允许再次点击。

```js
import { takeLeading, call, put } from 'redux-saga/effects';

// 模拟表单提交接口
const submitFormApi = (formData) => {
  return new Promise((resolve) => {
    setTimeout(() => resolve({ success: true }), 2000);
  });
};

function* submitFormSaga(action) {
  try {
    yield put({ type: 'SUBMIT_LOADING' }); // 禁用按钮
    const res = yield call(submitFormApi, action.payload);
    yield put({ type: 'SUBMIT_SUCCESS', payload: res });
  } catch (e) {
    yield put({ type: 'SUBMIT_FAILURE', payload: e.message });
  } finally {
    yield put({ type: 'SUBMIT_FINISH' }); // 启用按钮
  }
}

// takeLeading：只执行第一次请求，后续请求直到当前完成才会处理
export function* watchSubmitForm() {
  yield takeLeading('SUBMIT_FORM', submitFormSaga);
}
```

**效果**：用户连续点击提交按钮，只会执行第一次请求，直到请求完成后，再次点击才会生效。

#### 3.多请求并行执行（all）

**场景**：页面初始化需要同时请求 “用户信息” 和 “商品列表”，等两个请求都完成后再渲染页面。

```js
import { all, call, put } from 'redux-saga/effects';

// 模拟两个独立接口
const fetchUserApi = () => Promise.resolve({ name: '张三' });
const fetchGoodsApi = () => Promise.resolve([{ id: 1, name: '商品1' }]);

function* initPageSaga() {
  try {
    yield put({ type: 'INIT_LOADING' });
    // all：并行执行多个异步操作，全部完成后才继续
    const [user, goods] = yield all([
      call(fetchUserApi),
      call(fetchGoodsApi)
    ]);
    // 两个请求都完成后，更新状态
    yield put({ type: 'INIT_SUCCESS', payload: { user, goods } });
  } catch (e) {
    yield put({ type: 'INIT_FAILURE', payload: e.message });
  }
}

export function* watchInitPage() {
  yield takeLatest('INIT_PAGE', initPageSaga);
}
```

**效果**：两个接口同时请求（总耗时取最长的那个，而非相加），全部完成后才触发成功 action。

#### 4.接口轮询（定时重复请求）

**场景**：实时刷新数据（比如订单状态、实时监控数据），每隔 5 秒请求一次接口。

```js
import { take, call, put, delay, cancel, fork } from 'redux-saga/effects';

// 模拟轮询接口
const fetchRealTimeDataApi = () => Promise.resolve({ time: new Date().getTime() });

// 轮询逻辑
function* pollDataSaga() {
  while (true) { // 无限循环实现轮询
    try {
      const data = yield call(fetchRealTimeDataApi);
      yield put({ type: 'POLL_SUCCESS', payload: data });
    } catch (e) {
      yield put({ type: 'POLL_FAILURE', payload: e.message });
    }
    // 延迟 5 秒后再次请求
    yield delay(5000);
  }
}

// 启动/停止轮询的监听
export function* watchPollData() {
  let task;
  // 监听启动/停止 action
  while (true) {
    yield take('START_POLL'); // 监听启动轮询的 action
    task = yield fork(pollDataSaga); // 后台启动轮询任务
    yield take('STOP_POLL'); // 监听停止轮询的 action
    yield cancel(task); // 取消轮询任务
  }
}
```

**使用方式**：

- 组件 `dispatch ({type: 'START_POLL'})` 启动轮询；
- 组件 `dispatch ({type: 'STOP_POLL'})` 停止轮询；
    
**效果**：启动后每隔 5 秒请求一次接口，停止后立即终止轮询。

#### 5.请求失败重试（自动重试 3 次）

**场景**：接口请求偶尔失败（网络波动），自动重试 3 次，仍失败则提示用户。

```js
import { call, put, delay } from 'redux-saga/effects';

// 模拟易失败的接口（50% 概率失败）
const fetchUnstableApi = () => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      Math.random() > 0.5 ? resolve({ success: true }) : reject(new Error('请求失败'));
    }, 500);
  });
};

function* fetchWithRetrySaga() {
  const maxRetries = 3; // 最大重试次数
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const data = yield call(fetchUnstableApi);
      yield put({ type: 'FETCH_RETRY_SUCCESS', payload: data });
      return; // 成功则退出
    } catch (e) {
      retries++;
      if (retries >= maxRetries) {
        // 重试次数用尽，触发失败 action
        yield put({ type: 'FETCH_RETRY_FAILURE', payload: '重试3次仍失败' });
        return;
      }
      // 重试前延迟 1 秒（避免频繁请求）
      yield delay(1000);
      yield put({ type: 'FETCH_RETRY_RETRYING', payload: `第${retries}次重试` });
    }
  }
}

export function* watchFetchWithRetry() {
  yield takeLatest('FETCH_WITH_RETRY', fetchWithRetrySaga);
}
```

效果：接口失败后自动重试，最多 3 次，每次重试间隔 1 秒，重试过程中可向组件反馈重试状态。

#### 6.竞态请求（取最快返回的结果）

```js
import { race, call, put, cancel } from 'redux-saga/effects';

// 模拟两个不同速度的接口
const fetchFromMainApi = () => Promise.resolve('主站数据').then(res => delay(1000).then(() => res)); // 1秒返回
const fetchFromBackupApi = () => Promise.resolve('备用站数据').then(res => delay(500).then(() => res)); // 0.5秒返回

function* fetchRaceDataSaga() {
  try {
    yield put({ type: 'RACE_LOADING' });
    // race：竞态执行，谁先完成就用谁的结果，取消另一个
    const { main, backup } = yield race({
      main: call(fetchFromMainApi),
      backup: call(fetchFromBackupApi)
    });

    // 取最快返回的结果
    const data = backup || main;
    yield put({ type: 'RACE_SUCCESS', payload: data });
  } catch (e) {
    yield put({ type: 'RACE_FAILURE', payload: e.message });
  }
}

export function* watchFetchRaceData() {
  yield takeLatest('FETCH_RACE_DATA', fetchRaceDataSaga);
}
```

效果：备用站接口 0.5 秒返回，主站接口被自动取消，最终使用备用站的数据。

#### 7.总结

1. redux-saga 通过 `takeLatest/takeLeading` 解决重复请求问题，`all/race` 解决多请求协调问题；
2. 基于 `while(true) + delay` 可实现轮询，结合 `fork/cancel` 可灵活启停异步任务；
3. 通过循环 + `call` 可实现请求重试，`race` 可实现竞态请求，这些场景原生 Redux 几乎无法优雅实现；
4. 核心优势：所有复杂流程都集中在 saga 中，组件只需触发 action，完全解耦且易维护。

### 异步逻辑可测试、易调试

redux-saga 基于 Generator 函数，异步逻辑可以同步测试（不用模拟定时器 / 网络）：

```js
// 测试 saga 逻辑（同步执行，无需真实请求）
const gen = fetchUserSaga({ payload: 1 });
// 一步步验证 Generator 的执行结果
expect(gen.next().value).toEqual(put({ type: 'FETCH_USER_LOADING' }));
expect(gen.next().value).toEqual(call(fetchUserApi, 1));
```

### 统一的错误处理

```js
function* fetchUserSaga(action) {
  try {
    // 异步逻辑
  } catch (e) {
    // 统一处理错误（比如上报、提示、重置状态）
    yield put({ type: 'GLOBAL_ERROR', payload: e });
    yield call(showErrorToast, e.message);
  }
}
```

## 4.什么时候可以不用 redux-saga？

redux-saga 不是 “必选”，以下场景完全可以不用：

1. **小型项目**：只有少量简单异步请求（比如几个列表接口），用 Redux + redux-thunk（更轻量的中间件）就够了；
2. **无复杂流程**：不需要取消请求、轮询、多请求协调，异步逻辑只有「请求 - 成功 - 失败」三步；
3. **状态管理需求低**：甚至可以不用 Redux，直接用 React 的 `useState`/`useContext` + 自定义 hooks 管理状态。


# dva

[官网](https://github.com/dvajs/dva/blob/master/README_zh-CN.md)

dva 是基于 React + Redux + Redux-saga + React-Router 封装的轻量级前端框架，由阿里团队开发，目的是简化 React 项目中状态管理、路由、异步处理的配置和使用成本，让开发者能用更少的代码实现复杂应用。

## 为什么需要 dva？

使用原生 Redux + Redux-saga 时，你需要配置很多内容：

```js
// 原生写法：需要配置 store、saga、reducer
import { createStore, combineReducers, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';
import rootSaga from './sagas';
import userReducer from './reducers/user';
import productReducer from './reducers/product';

// 1. 创建 saga 中间件
const sagaMiddleware = createSagaMiddleware();

// 2. 合并 reducers
const rootReducer = combineReducers({
  user: userReducer,
  product: productReducer,
});

// 3. 创建 store
const store = createStore(rootReducer, applyMiddleware(sagaMiddleware));

// 4. 启动 saga
sagaMiddleware.run(rootSaga);
```

使用 dva 后：

```js
// dva 写法：一个配置搞定
import dva from 'dva';

const app = dva();

app.model({
  namespace: 'user',
  state: { name: '张三' },
  effects: {
    *fetchUser({ payload }, { call, put }) {
      const data = yield call(fetchUserApi, payload);
      yield put({ type: 'save', payload: data });
    },
  },
  reducers: {
    save(state, { payload }) {
      return { ...state, ...payload };
    },
  },
});

app.router(({ history }) => <Router history={history} routes={routes} />);
app.start('#root');
```

## dva 核心概念

dva 的核心是 **Model**，一个 Model 包含了一个业务模块的所有逻辑：

```
Model
├── namespace     # 命名空间（全局 state 的 key）
├── state         # 初始状态
├── reducers      # 同步更新状态（纯函数）
├── effects       # 异步处理（基于 redux-saga）
├── subscriptions # 订阅数据源（监听键盘、路由、websocket 等）
```

### 数据流

```
UI 交互触发 dispatch
    ↓
触发 action (type + payload)
    ↓
如果有对应的 effect，先执行 effect（异步）
    ↓
effect 内部 call API，然后 put 触发 reducer
    ↓
reducer 纯函数更新 state
    ↓
state 变化触发 UI 重新渲染
```

## 核心功能

### 1. Model - 业务逻辑单元

Model 是 dva 的核心，将 state、reducer、effect、subscription 整合在一起：

```js
app.model({
  namespace: 'products',  // 全局 state 的 key，即 state.products
  state: {                // 初始状态
    list: [],
    loading: false,
  },
  // reducers：同步更新状态（纯函数）
  reducers: {
    save(state, { payload }) {
      return { ...state, ...payload };
    },
    setLoading(state, { payload }) {
      return { ...state, loading: payload };
    },
  },
  // effects：异步处理（基于 redux-saga）
  effects: {
    *fetchProducts({ payload }, { call, put }) {
      yield put({ type: 'setLoading', payload: true });
      const data = yield call(fetchProductsApi, payload);
      yield put({ type: 'save', payload: { list: data, loading: false } });
    },
  },
  // subscriptions：订阅外部数据源
  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/products') {
          dispatch({ type: 'fetchProducts' });
        }
      });
    },
  },
});
```

### 2. Effects - 异步处理

effects 基于 redux-saga，支持所有 saga 的能力：

```js
effects: {
  // 基本用法
  *fetchUser({ payload }, { call, put }) {
    const res = yield call(api.getUser, payload);
    yield put({ type: 'save', payload: res });
  },

  // 并行请求
  *fetchAll(_, { call, put, all }) {
    const [users, products] = yield all([
      call(api.getUsers),
      call(api.getProducts),
    ]);
    yield put({ type: 'save', payload: { users, products } });
  },

  // 取消重复请求（takeLatest）
  *fetchData: [
    function* ({ payload }, { call, put }) {
      const data = yield call(api.fetchData, payload);
      yield put({ type: 'save', payload: data });
    },
    { type: 'takeLatest' },  // 自动取消前一次未完成的请求
  ],

  // 只执行第一次（takeLeading）
  *submitForm: [
    function* ({ payload }, { call, put }) {
      yield call(api.submitForm, payload);
      yield put({ type: 'submitSuccess' });
    },
    { type: 'takeLeading' },
  ],
}
```

### 3. Subscriptions - 订阅外部数据源

subscriptions 用于订阅外部输入，如键盘事件、路由变化、websocket 等：

```js
subscriptions: {
  // 监听键盘事件
  setupKeydown({ dispatch }) {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        dispatch({ type: 'modal/close' });
      }
    });
  },

  // 监听路由变化
  setupHistory({ dispatch, history }) {
    history.listen(({ pathname, query }) => {
      if (pathname === '/search') {
        dispatch({ type: 'search/fetch', payload: query });
      }
    });
  },

  // 监听 websocket
  setupWebSocket({ dispatch }) {
    const ws = new WebSocket('ws://localhost:8080');
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      dispatch({ type: 'websocket/message', payload: data });
    };
  },
}
```

### 4. Connect - 连接组件和状态

使用 `connect` 将 Model 的 state 和 dispatch 绑定到组件：

```js
import { connect } from 'dva';

const UserList = ({ users, loading, dispatch }) => {
  useEffect(() => {
    dispatch({ type: 'users/fetch', payload: { page: 1 } });
  }, []);

  if (loading) return <div>加载中...</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};

// 将 model 的 state 和 dispatch 映射到 props
export default connect(({ users }) => ({
  users: users.list,
  loading: users.loading,
}))(UserList);
```

## 快速入门案例

### 需求

实现一个简单的「待办事项」应用：

- 添加待办事项
- 删除待办事项
- 切换完成状态
- 统计未完成数量

### 1. 项目初始化

```bash
# 安装 dva-cli
npm install dva-cli -g

# 创建项目
dva new todo-app
cd todo-app

# 启动开发服务器
npm start
```

### 2. 定义 Model

创建 `src/models/todos.js`：

```js
export default {
  namespace: 'todos',
  state: {
    list: [],
  },
  reducers: {
    // 添加待办
    add(state, { payload: text }) {
      return {
        list: [
          ...state.list,
          { id: Date.now(), text, completed: false },
        ],
      };
    },
    // 删除待办
    remove(state, { payload: id }) {
      return {
        list: state.list.filter(item => item.id !== id),
      };
    },
    // 切换完成状态
    toggle(state, { payload: id }) {
      return {
        list: state.list.map(item =>
          item.id === id ? { ...item, completed: !item.completed } : item
        ),
      };
    },
  },
};
```

### 3. 创建组件

创建 `src/components/Todos.js`：

```js
import React, { useState } from 'react';
import { connect } from 'dva';

const Todos = ({ list, dispatch }) => {
  const [inputValue, setInputValue] = useState('');

  const handleAdd = () => {
    if (!inputValue.trim()) return;
    dispatch({ type: 'todos/add', payload: inputValue });
    setInputValue('');
  };

  const handleRemove = (id) => {
    dispatch({ type: 'todos/remove', payload: id });
  };

  const handleToggle = (id) => {
    dispatch({ type: 'todos/toggle', payload: id });
  };

  const uncompletedCount = list.filter(item => !item.completed).length;

  return (
    <div style={{ padding: 20 }}>
      <h1>待办事项 ({uncompletedCount} 未完成)</h1>

      <div>
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
          placeholder="输入待办事项"
        />
        <button onClick={handleAdd}>添加</button>
      </div>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {list.map((todo) => (
          <li key={todo.id} style={{ margin: 10 }}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => handleToggle(todo.id)}
            />
            <span
              style={{
                textDecoration: todo.completed ? 'line-through' : 'none',
                marginLeft: 10,
              }}
            >
              {todo.text}
            </span>
            <button
              onClick={() => handleRemove(todo.id)}
              style={{ marginLeft: 10 }}
            >
              删除
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default connect(({ todos }) => ({
  list: todos.list,
}))(Todos);
```

### 4. 配置路由

修改 `src/router.js`：

```js
import React from 'react';
import { Router, Route, Switch } from 'dva/router';
import Todos from './components/Todos';

const RouterConfig = ({ history }) => {
  return (
    <Router history={history}>
      <Switch>
        <Route path="/" exact component={Todos} />
      </Switch>
    </Router>
  );
};

export default RouterConfig;
```

### 5. 注册 Model

修改 `src/index.js`：

```js
import dva from 'dva';
import './index.css';

// 1. 初始化
const app = dva();

// 2. 注册 plugins（可选）
// app.use({});

// 3. 注册 model
app.model(require('./models/todos').default);

// 4. 注册 router
app.router(require('./router').default);

// 5. 启动应用
app.start('#root');
```

### 6. 完整效果

运行 `npm start` 后，你将获得：

- ✅ 可添加待办事项
- ✅ 点击复选框切换完成状态
- ✅ 点击删除按钮移除待办
- ✅ 实时显示未完成数量

## 带异步请求的完整案例

### 需求

从 API 获取用户列表并展示：

```js
// models/users.js
export default {
  namespace: 'users',
  state: {
    list: [],
    loading: false,
    error: null,
  },
  effects: {
    // 获取用户列表（异步）
    *fetchUsers(_, { call, put }) {
      try {
        yield put({ type: 'setLoading', payload: true });
        const res = yield call(
          () => fetch('https://jsonplaceholder.typicode.com/users')
            .then(r => r.json())
        );
        yield put({ type: 'save', payload: { list: res } });
      } catch (e) {
        yield put({ type: 'setError', payload: e.message });
      } finally {
        yield put({ type: 'setLoading', payload: false });
      }
    },
  },
  reducers: {
    save(state, { payload }) {
      return { ...state, ...payload };
    },
    setLoading(state, { payload }) {
      return { ...state, loading: payload };
    },
    setError(state, { payload }) {
      return { ...state, error: payload };
    },
  },
  subscriptions: {
    setup({ dispatch, history }) {
      // 进入页面自动获取数据
      return history.listen(({ pathname }) => {
        if (pathname === '/users') {
          dispatch({ type: 'fetchUsers' });
        }
      });
    },
  },
};

// components/UserList.js
import React, { useEffect } from 'react';
import { connect } from 'dva';

const UserList = ({ list, loading, dispatch }) => {
  useEffect(() => {
    dispatch({ type: 'users/fetchUsers' });
  }, []);

  if (loading) return <div>加载中...</div>;

  return (
    <div>
      <h1>用户列表</h1>
      <ul>
        {list.map(user => (
          <li key={user.id}>
            {user.name} ({user.email})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default connect(({ users }) => ({
  list: users.list,
  loading: users.loading,
}))(UserList);
```

## dva vs 原生 Redux

| 特性 | 原生 Redux + Saga | dva |
|------|------------------|-----|
| 代码组织 | 分散在多个文件 | Model 集中管理 |
| 配置复杂度 | 高（需要配置 store、middleware、saga） | 低（一行代码启动） |
| 学习曲线 | 陡峭（需要理解 reducer、saga、effect） | 平缓（统一的 Model 概念） |
| 代码量 | 多 | 少约 40-60% |
| 适合场景 | 中大型项目、需要高度定制 | 快速开发、中小型项目 |

## 总结

1. **dva 的核心价值**：通过 Model 概念统一 state、reducer、effect、subscription，大幅简化 Redux 开发
2. **数据流清晰**：dispatch → effect（异步）→ reducer（同步）→ state → UI
3. **开发体验好**：配置简单、代码量少、易于维护
4. **适合场景**：中后台应用、快速原型开发、React 状态管理入门

