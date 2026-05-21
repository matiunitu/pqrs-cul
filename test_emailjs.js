const data = {
  service_id: 'service_25libn5',
  template_id: 'template_tu878js',
  user_id: 'o3tsRNH8slV7K4jTP',
  template_params: {
    name: 'Test User',
    title: 'Test Radicado RAD-12345',
    email: 'test@example.com'
  }
};

fetch('https://api.emailjs.com/api/v1.0/email/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  },
  body: JSON.stringify(data)
})
.then(async res => {
  const text = await res.text();
  console.log('Status:', res.status);
  console.log('Response:', text);
  if (res.status === 200) {
    console.log('EmailJS is working correctly!');
  } else {
    console.log('EmailJS is NOT working correctly.');
  }
})
.catch(err => {
  console.error('Error:', err);
});
