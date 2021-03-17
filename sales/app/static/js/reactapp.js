'use strict';
const e = React.createElement;

function App() {
  const [text, setText] = React.useState("123");
  console.log("In da app");
  return (
    <div>
      <Welcome name="Hello" />
      <Welcome name="World" />
      <Welcome name={text} click={()=>{setText("234"); console.log("click")}}/>
    </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
