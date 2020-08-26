library(rtweet)
library(tidyverse)
library(httr)
library(imager)

grant_access <- function(path_to_file){
  tryCatch(
    expr = {
      file <- readLines(path_to_file)
      api_key <- str_trim(unlist(str_split(file[1], "="))[2], "both")
      api_secret_key <- str_trim(unlist(str_split(file[2], "="))[2], "both")
      access_token <- str_trim(unlist(str_split(file[3], "="))[2], "both")
      access_token_secret <- str_trim(unlist(str_split(file[4], "="))[2], "both")
      
      token <<- create_token(app = "ElvaBot", consumer_key = api_key, consumer_secret = api_secret_key, access_token = access_token, access_secret = access_token_secret)
      get_token()
      message("If keys were given correctly, access should be granted now!")
    },
    error = function(e){
      message("Error: Check if path to file exists...")
    }
  )
}


download_profile_photo <- function(username, downloads_path, show_image = FALSE){
  if(exists("token") == FALSE){
    stop("You should grant access to Twitter API as a first step! Please, use 'grant_access()'.")
  }
  else{
    user_info <- lookup_users(username)
    if(dim(user_info)[1] == 0){
      stop("Error: The provided user does not exists or perhaps the account is private.")
    }
    else{
      profile_image_url <- user_info[[which(names(user_info) == "profile_image_url")]]
      profile_image_url <- str_replace_all(profile_image_url, "_normal", "")
      GET(profile_image_url, write_disk(paste0(downloads_path, "/", username, "_photo.jpg")))
    }
    
    if(show_image == TRUE){
      im <- load.image(paste0(downloads_path, "/", username, "_photo.jpg"))
      plot(im, ann = FALSE, axes = FALSE)
    }
  }
}










