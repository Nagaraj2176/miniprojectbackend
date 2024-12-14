let connectelement=document.querySelector('.connect');
let names=['Connect.','Connect.....'];

let namecount=0;
let lettercount=0;

textmove();

function textmove()
{
  connectelement.innerHTML=`${names[namecount].slice(0,lettercount)}`;
  

  if(lettercount===names[namecount].length)
  {
    namecount++;
    lettercount=0;
  }
  if(namecount===names.length)
  {
    namecount=0;
  }
  lettercount++;

  setTimeout(()=>{
    textmove()
  },600)
}

const observer= new IntersectionObserver((entries)=>{
  entries.forEach((entry)=>{
    if(entry.isIntersecting)
    {
      entry.target.classList.add('show');
    }
    else{
      entry.target.classList.remove('show');
    }
  })
});

let contentelement=document.querySelectorAll('.animatetext');

contentelement.forEach((elem)=>{
  observer.observe(elem);
});


