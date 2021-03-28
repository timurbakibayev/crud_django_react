'use strict';
const e = React.createElement;

function App() {
  const [text, setText] = React.useState("123");

  const getData = async ()=>{
    const serializedCredentials = localStorage.getItem("salesLogin");
    console.log(serializedCredentials);
    if (serializedCredentials === null) {
      console.log("No credentials found, redirecting...");
      window.location = "/login";
    }
  };

  getData();

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
