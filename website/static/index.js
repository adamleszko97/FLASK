function deleteEmployee(employeeId) {
    console.log(employeeId);
    
    fetch("/delete-employee", {
      method: "POST",
      body: JSON.stringify({ employeeId: employeeId }),
    }).then((_res) => {
      window.location.href = "/search";
    });
    debugger;
  }