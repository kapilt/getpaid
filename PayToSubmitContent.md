An authenticated user on the site adds a piece of content of the type "Pay to Submit". The user can work on the content and save a draft. When the user is ready to finish the content, the user "Submits" the content. The content's state is changed to "Pending Payment" and a portal message at the top of the page notifies the user that "Payment is necessary to complete the submission. Please click here to pay now". The link leads to user to a checkout process. Upon successful completion of checkout, the workflow state on the object is updated to "published". If the checkout is unsuccessful or the user does not click the link, the object remains in the pending state and the user can return later to complete the checkout.


---

Draft of implementation idea by perrito and javier

---


Recently I have been presented with the need to make getpaid charge for
content to be uploaded to a site. After a few rounds of planning with
javimansilla we came up with an idea that we believe could satisfy more than
one need in the GetPaid comunity.

The idea is the following.
On the admin screen of getpaid you have a section for "pay for submit" content
this features a list of content types in a widget similar to the one presented
for selecting types for buyable, etc types.
Then you have two entries where you will input two workflow transitions one to
capture and one to trigger when the checkout is complete.
On the other hand we can not do that to all existing objects of the same type,
that would make this method a little intrussive so this is how it works on the
user end.
First admin need to create a folderish object or just pick one existing and he
will have the "make pay submittable" (or a name some one that speaks better
english than I can come with) so inside that folder each time you try to
trigger the transition specified in the admin screen on one of the objects
specified in the admin screen (lets say submit an Image) so when the image
owner tries to trigger submit he is redirected to the checkout screen (we may
use oneshot cart created for getpaid.formgen in order not o interfere with
users preexisting cart) so if the user ends a successful checkout we will then
triger the specified transition.
We could add some features for the admin to specify if this is going to happen
always or only when the user does it the first time or if there is going to be
a period of validity (this may take a little more work).
This is the less intrussive way javier and I could think about to add this
feature, we wouldn't be imposing custom workflows or anything else, and only
affect files under activated folders.