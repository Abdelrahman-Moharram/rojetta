function addSkill(){
    var skillsLi = null;
    skillsLi = document.getElementById('skillsLi');
    skillsLi.innerHTML += `
    <div class="row my-4">
                <div class="col-4">
                  <div class="dropdown mb-4">
                  <div
                    class="dropdown-toggle d-flex align-items-center hidden-arrow"
                    id="SkillTypesMenuAvatar"
                    role="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                  >
                  <div class="form-outline">
                    <input value="" name="skill_type"  type="text" id="form3skill_type" class="form-control" />
                    <label class="form-label" for="form3Bio">skill type</label>
                  </div>
                  </div>
                  <ul
                    class="dropdown-menu w-100"
                    aria-labelledby="SkillTypesMenuAvatar"
                  >
                  
                  '{% for type in SkillTypes %}'
                    <li>
                      <div onclick="changeValId('{{type.name}}', 'form3skill_type')" class="dropdown-item">
                        <span class="mx-3">'{{type.name}}'</span>
                      </div>
                    </li>
                  '{% endfor %}'
                  </ul>
                </div>
                </div>
                <div class="col-8 mb-4">
                  <div class="form-outline">
                    <input value="" name="skill" type="text" id="form3Example2" class="form-control" />
                    <label class="form-label" for="form3Example2">skill</label>
                  </div>
                </div>
                <div class="col-12 mb-4">
                  <div class="form-outline">
                    <input value="" name="skill_date" type="date" id="form3Example2" class="form-control" />
                    <label class="form-label" for="form3Example2">date</label>
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-outline">
                    <input value="" name="certificate" type="file" id="form3Example2" class="form-control" />
                    <label class="form-label" for="form3Example2">certificate</label>
                  </div>
                </div>
                <hr>
              </div>
    `;
  }


  function changeValId(val, id, boolValue) {
    document.getElementById(id).value = val;
    if (boolValue){
        getStates()
        let statesList = document.getElementById("statesListAvatar")
        statesList.innerHTML = '';
    }
  }

  function getStates(){
    flag = false
    var gover = document.getElementById('form3government').value
    console.log(gover);
    $.ajax({
      url:'/accounts/getStates/'+gover+"/",
      type:'GET',
      success: function(data){
        let statesList = document.getElementById("statesListAvatar")
        // statesList.innerHTML = `
        // <li>
        //     <div onclick="changeValId('{{state.name}}', 'form3government')" class="dropdown-item">
        //         <span class="mx-3">{{government.name}}</span>
        //     </div>
        // </li>
        //           `;
        data.states.forEach(state => {
          statesList.innerHTML+=`
            <li>
                <div onclick="changeValId('${state.name}', 'form3state')" class="dropdown-item">
                    <span class="mx-3">${state.name}</span>
                </div>
            </li>
                  `
        });
      },
      error: function(errs){
        console.error("errors=>", errs);
      }
    })
  }

  function addPhone(){
    var skillsLi = null;
    skillsLi = document.getElementById('PhoneItem');
    skillsLi.innerHTML += `
    <br>
    <div class="col form-outline">
            <input name="phone" type="text" id="form3phone" class="form-control" />
            <label class="form-label" for="form3Bio">phone</label>
    </div>
    `;
  }

  MyBanners=[
    '/static/imgs/background-1.avif',
    'https://mdbootstrap.com/img/Photos/Others/images/37.jpg',
    '/static/imgs/background-2.avif',
  ]
  banner=0


  function ShowBanners(){ 
    var bannerImage = document.getElementById('banner')
    if (document.images){
      banner++
      if (banner==MyBanners.length) {
        banner=0
      }
      bannerImage.style.backgroundImage= "url('"+MyBanners[banner]+"')"
      setTimeout("ShowBanners()",5000)
  }
}
function previousImage() {
      var bannerImage = document.getElementById('banner')
        if(count!=0){
          count--;
        }
        else if(banner==0){
          banner=MyBanners.length
        }
        bannerImage.style.backgroundImage= "url('"+MyBanners[banner]+"')";
        setTimeout("ShowBanners()",5000)

}
function nextImage() {
    if(count!=4)
        count++;
    else if(banner==MyBanners.length){
        banner=0
    }
    var id = document.getElementById("imageId");
    id.src = "images/" + images[count];
  }
  // setTimeout("ShowBanners()",5000);