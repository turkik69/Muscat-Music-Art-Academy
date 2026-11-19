const menuButton=document.querySelector('.menu-button');
const nav=document.querySelector('.site-nav');
if(menuButton&&nav){
  menuButton.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));});
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}});
}
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
const enquiry=document.getElementById('enquiry-form');
if(enquiry) enquiry.addEventListener('submit',event=>{
  event.preventDefault();if(!enquiry.reportValidity())return;
  const lang=enquiry.dataset.lang;
  const name=enquiry.elements.namedItem('name').value.trim();
  const interest=enquiry.elements.namedItem('interest');
  const age=enquiry.elements.namedItem('age');
  const note=enquiry.elements.namedItem('note').value.trim();
  if(!name)return;
  const choice=select=>select.options[select.selectedIndex].textContent;
  const lines=lang==='ar'?['مرحبًا، أود الاستفسار عن الالتحاق بأكاديمية مسقط للموسيقى والفنون.',`الاسم: ${name}`,`المجال: ${choice(interest)}`,`الفئة العمرية: ${choice(age)}`]:['Hello, I would like to enquire about joining Muscat Music & Art Academy.',`Name: ${name}`,`Area of interest: ${choice(interest)}`,`Age group: ${choice(age)}`];
  if(note)lines.push((lang==='ar'?'ملاحظات: ':'Notes: ')+note);
  const url='https://wa.me/96871498887?text='+encodeURIComponent(lines.join('\n'));
  window.location.assign(url);
});
