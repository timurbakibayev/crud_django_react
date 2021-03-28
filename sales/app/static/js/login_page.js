'use strict';
const e = React.createElement;

function App() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const tryLogin = async (e) => {
    e.preventDefault();
    console.log("Loggin in with", username, password);
  };

  return (
      <div style={{width: "400px", margin: "auto", marginTop: "200px",
        boxShadow: "2px 5px 2px 2px #cccccccc",
        padding: "1em"
                }}>
        <form>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Username</label>
            <input type="text" className="form-control" id="username" placeholder="username"
              onChange={(e)=>{setUsername(e.target.value)}} value={username}/>
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input type="password" className="form-control" id="password" placeholder="password"
              onChange={(e)=>{setPassword(e.target.value)}} value={password}/>
          </div>
          <button type="submit" className="btn btn-primary" onClick={tryLogin}>Login</button>
        </form>
      </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
