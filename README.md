# Housing Yelp

### How's our build?

[![Build Status](https://travis-ci.com/UVA-CS3240-S19/project-101-five-fishy-fishermen.svg?token=Kpx8qxw1sbsdXyhVxRq3&branch=master)](https://travis-ci.com/UVA-CS3240-S19/project-101-five-fishy-fishermen)


### File Storage

We implemented blob storage through the Google Cloud API by following [this tutorial](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html).


# Welcome to HOOS' HOUSING!
To get started, visit our website at https://peaceful-river-84513.herokuapp.com/ and sign in with google by clicking the "Log In" button in the top right corner of the NavBar. Building pages and reviews can be viewed without logging in, but you must be logged in to leave a review, rate reviews, and add favorites

## Home Page
From the homepage you can see all of the different buildings where students at UVa can live. Click on the names of one of these buildings to view the building detail page, or if you have a new building to add, click the "Add a Building" button at the top of the page. Buildings must be approved by the staff, so your building will not appear immediately after submitting. Please allow 5-7 business days for this.

## Building Detail Page
The building detail page is the page assigned to each building that contains lists of amenities, contact information, units available, price, and address. There is also a map that automatically displays the location of the building. 
### Favorites
This is the page where you can favorite the building by clicking the heart next to the building name at the top of the page; however, you must be logged on to use this feature. You can view your favorites by clicking the dropdown menu in the top right of the NavBar that has your name as the title. "Favorites" is an option in the list.
### Reviews
Reviews for each building can be found at the bottom of its building detail page. You can sort these reviews by most recent, most helpful, highest rating, and lowest rating by clicking the "Sort by" dropdown menu. You can upvote reviews you find helpful by clicking the arrow to the left of each review. It will turn yellow when you have upvoted it. Click on the arrow again to undo your upvote. The number of people who have upvoted appears below the arrow.

You can also add your own review by clicking the "Leave a review" button below all of the reviews. Enter your rating, a title for the review, and the review text and hit submit. Your review will automatically appear on the page. You can view all the reviews you have submitted by clicking the dropdown menu in the top right of the NavBar that has your name as the title. "Reviews" is an option in the list.

## Review Buildings
If you are an admin, you have the ability to review buildings using the "Review Buildings" tab in the NavBar. From here you can publish and unpublish current buildings. Unpublished buildings do not show up on the home page.



