const url = "127.0.0.1"


async function savefile(inp) 
{
    let formData = new FormData();
    let file = inp.files[0];      
    
    formData.append(file.name, file);
    
    try {
       let r = await fetch('/video', {method: "POST", body: formData}); 
       console.log('HTTP response code:',r.status); 
    } catch(e) {
       console.log('we have problem...:', e);
    }
    
}