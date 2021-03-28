'use strict';
const e = React.createElement;

function App() {
  const [list, setList] = React.useState([]);

  const success = (data) => {
    setList(data.data);
  };

  const logout = async (e)=>{
    await localStorage.setItem("salesToken",null);
    window.location = "/login";
  };

  const getData = async ()=>{
    await get_data_api(0, success, (text)=>{console.log("Error: ", text)})
  };

  React.useEffect(getData,[]);

  return (
    <div>
      <div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
        boxShadow: "5px 5px 20px #cccccccc",
        padding: "1em"
                }}>
        <div style={{display: "flex", flexDirection: "row"}}>
          <span>Super Sales App</span>
          <a className="btn btn-light" style={{marginLeft: "auto"}} onClick={logout}>Logout</a>
        </div>
      </div>
      <div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
        boxShadow: "5px 5px 20px #cccccccc",
        padding: "1em"
                }}>
        <div style={{display: "flex", flexDirection: "row", marginBottom: "5px"}}>
          <a className="btn btn-light" style={{marginLeft: "auto"}}>New Sale</a>
        </div>
        <table className="table table-hover caption-top">
          <thead className="table-light">
          <tr>
            <th>id</th>
            <th>Date</th>
            <th>Item</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Amount</th>
            <th>Action</th>
          </tr>
          </thead>
          <tbody>
          { list.map((row)=>
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.date}</td>
              <td>{row.item}</td>
              <td>{row.price}</td>
              <td>{row.quantity}</td>
              <td>{row.amount}</td>
              <td>Edit</td>
            </tr>
          )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
