// Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  var firebaseConfig = {
    apiKey: "AIzaSyCBRDuijlf1mylK3f9WHVbSRv8emWZD4S8",
    authDomain: "cisco-hack.firebaseapp.com",
    projectId: "cisco-hack",
    storageBucket: "cisco-hack.appspot.com",
    messagingSenderId: "833619410187",
    appId: "1:833619410187:web:8e0f13ef65b252a94f760e",
    measurementId: "G-4WLK0G0QX6"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();

  const fileInput = document.getElementById('upload');
  fileInput.onchange = () => {
    let selectedFile = fileInput.files[0];
    console.log(selectedFile)
    const ref = firebase.storage().ref();
    const name = (+new Date()) + '-' + selectedFile.name;
    const metadata = { contentType : selectedFile.tpye};
    const task = ref.child(name).put(selectedFile,metadata);
  }