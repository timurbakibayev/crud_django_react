'use strict';
const e = React.createElement;

function Welcome(props) {
  return <h1>Привет, {props.name}</h1>;
}

function App() {
  console.log("In da app")
  return (
    <div>
      <Welcome name="Алиса" />
      <Welcome name="Базилио" />
      <Welcome name="Буратино" />
    </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
// ReactDOM.render(e(MyReactApp), domContainer);
