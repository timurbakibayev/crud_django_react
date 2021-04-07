'use strict';
const e = React.createElement;

function App() {
  const [list, setList] = React.useState([]);
  const [showModal, setShowModal] = React.useState(false);
  const [modalDescription, setModalDescription] = React.useState("");
  const [itemId, setItemId] = React.useState(null);
  const [error, setError] = React.useState("");
  const [item, setItem] = React.useState("");
  const [price, setPrice] = React.useState(0);
  const [quantity, setQuantity] = React.useState(0);

  const success = (data) => {
    setList(data.data);
  };

  const logout = async (e)=>{
    await localStorage.setItem("salesToken",null);
    window.location = "/login";
  };

  const getData = ()=>{
    get_sales_api(0, success, (text)=>{console.log("Error: ", text)});
  };

  const newSale = ()=>{
    setModalDescription("New sale");
    setItemId(null);
    setItem("");
    setPrice(0);
    setQuantity(0);
    setError("");
    setShowModal(true);
    const itemInput = document.getElementById("itemInput");
    setTimeout(()=>{itemInput && itemInput.focus()}, 1);
  };

  const editSale = (data)=>{
    setModalDescription("New sale");
    setItemId(data.id);
    setItem(data.item);
    setPrice(data.price);
    setQuantity(data.quantity);
    setError("");
    setShowModal(true);
    const itemInput = document.getElementById("itemInput");
    setTimeout(()=>{itemInput && itemInput.focus()}, 1);
  };

  const saveSale = (e)=>{
    e.preventDefault();
    setError("");
    console.log("saving new", item, price, quantity);
    if (item.length * price * quantity === 0)
      setError("Please enter item name, price and quantity");
    else {
      if (itemId === null)
        post_sale_api({item, price, quantity}, ()=>{getData();});
      else
        put_sale_api(itemId, {item, price, quantity}, ()=>{getData();});
      setShowModal(false);
    }
  };

  const deleteSale = (saleId)=>{
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        delete_sale_api(saleId, ()=>{
          Swal.fire({
              title: 'Deleted!',
              text: "Your sale has been deleted!",
              icon: 'success',
              timer: 1000,
          });
          getData();
        });
      }
    });
  };

  const keyDownHandler = (e)=>{
    if (e.which === 27)
      setShowModal(false);
    if (e.which === 78 && !showModal)
      newSale();
  };

  React.useEffect(()=>{
    getData();
    document.addEventListener('keydown', keyDownHandler);
  },[]);

  return (
    <div onKeyDown={keyDownHandler}>
      <div style={{background: "#00000060"}}
          className={"modal " + (showModal?" show d-block":" d-none")} tabIndex="-1" role="dialog">
        <div className="modal-dialog shadow">
          <form method="post">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{modalDescription}</h5>
              <button type="button" className="btn-close" onClick={()=>{setShowModal(false)}} aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <label>Item name</label>
                <div className="form-group">
                  <input type="text" className="form-control" name="item" id="itemInput"
                         value={item} onChange={(e)=>{setItem(e.target.value)}}
                         placeholder="Item name"/>
                </div>
              <label style={{marginTop: "1em"}}>Price</label>
                <div className="form-group" >
                  <input type="number" className="form-control" placeholder="Price"
                         value={price} onChange={(e)=>{setPrice(e.target.value)}}
                         name="price" />
                </div>
              <label style={{marginTop: "1em"}}>Quantity</label>
                <div className="form-group">
                  <input type="number" className="form-control"
                         value={quantity} onChange={(e)=>{setQuantity(e.target.value)}}
                         placeholder="Quantity" name="quantity" />
                </div>
              <small className="form-text text-muted">{error}</small>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={()=>{setShowModal(false)}} data-bs-dismiss="modal">Close</button>
              <button type="submit" className="btn btn-primary" onClick={saveSale}>Save changes</button>
            </div>
          </div>
          </form>
        </div>
      </div>

      <div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
                    padding: "1em"}} className="shadow">
        <div style={{display: "flex", flexDirection: "row"}}>
          <span>Super Sales App</span>
          <a className="btn btn-light" style={{marginLeft: "auto"}} onClick={logout}>Logout</a>
        </div>
      </div>
      <div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
                    padding: "1em"}} className="shadow">
        <div style={{display: "flex", flexDirection: "row", marginBottom: "5px"}}>
          <a className="btn btn-light" style={{marginLeft: "auto"}}
             onClick={newSale}
          >New Sales Order</a>
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
              <td>
                <a className="btn btn-light" style={{marginLeft: "auto"}}
                  onClick={(e)=>{editSale(row)}}>Edit</a>{" "}
                <a className="btn btn-light" style={{marginLeft: "auto"}}
                  onClick={(e)=>{deleteSale(row.id)}}>Delete</a>
              </td>
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
