var edit = $('.pencil');
// var userChange = $('.userChange') //input for user
var username = $('.username')
// var email_input = $('.email_input')
var email = $('.email')
// var password_input = $('.password_input')
var password = $('.password')
// var bio_input = $('.bio_input')
var bio = $('.bio')
var text_secondary= $('.text-secondary')
// var user_input = $('.user_info_input')
var save_button = $('.save')



    edit.click(function(){
        edit.hide()
        save_button.show()
        text_secondary.attr('contenteditable','true')
})
    save_button.click(function(){
        
        // alert(username.text())
        save_button.hide()
        edit.show()

        text_secondary.attr('contenteditable','false')
        
    
        // text_secondary.show()
        // userChange.hide()
        // email_input.hide()
        // password_input.hide()
        // bio_input.hide()
        // save_button.hide()
      
    })

  



