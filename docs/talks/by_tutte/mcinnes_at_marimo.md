Transcript of 

EVoC is the new UMAP - with Leland McInnes!
https://www.youtube.com/watch?v=ES4PPjK21TM

Okay, YouTube says that we're live, but I have to confirm in the actual YouTube stream if that is indeed the case. So,
uh, let me just go in there and double check.
Okay, we are. Okay, so we're live. Uh, and we're um I guess even a little bit
early because um I think I set this to like 4:15 and um people might be joining
in super early, but that's kind of okay because uh that means we get to banther a little bit. Leland, hi. Uh welcome to
the live stream that we've kickstarted again. And um one thing I want to do is just introduce you a little bit. Um
because a while ago you made this thing called UMAP and it's kind of one of these I would also like almost argue uh
hidden gems in the old school data science ecosystem that's still very much around like people are still doing
things with embeddings and people are still doing things with um but then um a
few weeks ago uh I got a notification from Scott from Weights and Biases he's a colleague of mine um making me aware
of the fact that you've started doing something new and I think it's called Evok if I'm not mistaken Okay. And
sorry, evoke is Yeah. Yeah. Yeah. Ah, okay. But then the down the downside
of evoke, at least when I uh put it into the search engine over here, is it doesn't index very well just yet. That's
kind of correct. The downside. So, what I figured I might do is uh I'm just going to go ahead and
walk you through a notebook that I made that is going to uh you know, demonstrate the whole setup a little
bit. And after that, we're gonna actually use this uh evoke. We're gonna see some interesting things and then
we're gonna just, you know, um talk about how the algorithm works. And very very low effort on your end. Very much
I'm trying to demonstrate to you something. And then hopefully I'm also able to show you some u some neat tricks.
I'm I'm looking forward to the neat tricks. Yes. So, okay. So, we're going to be dealing with embeddings. And I think the
simplest way to get started is to do something with this fashion mnest. Um it's an old school data set. It's kind
of like emnest except it's all fashion items. That's kind of the the main big difference. And we have a feature for
every single pixel in this thing. So you can you can kind of make out some of the pixels here, right? That's a feature.
And uh you know it's it's not mega huge like we can come up with way bigger embeddings, but it might still be fun to
have like a smaller set of features. So historically what you would do is you would use something like umap or
something like uh PCA to take that super big dimensional space and to sort of make that a fair chunk smaller.
Um so I'm in a marima notebook and what I'm able to do is specify the number of samples uh that I'm going to train
everything on. I can specify the number of components and I can say whether or not we're going to use um or we're going to use PCA. The result of this is going
to be this principle like this parallel coordinates chart. And the thing that's pretty fancy, and I don't know if you saw this, is I'm able to make a
selection here, and then the component down below updates. Oh, that's nice. So, that's pretty cool, especially
because um what this allows us to do is not do like a rinky dink two-dimensional chart. No, no. We can go into way higher
dimensions. And one thing that's kind of neat here is you can very like clearly see these
different classes, right? So, you can actually see like, okay, the trousers here, those are all like super blue. We can see that there's like a streak that
moves around all these different uh coordinates. And for the folks at home, uh sort of re-watching this. Um and
actually grab my tablet device and tell it that I'm working on this screen. Um
but one thing to remember here is of course that like every single one of these is like a separate column. So
we've gone from hundreds of dimensions to just eight. This is the the first principal component. This is the second
one. Um, so most of the variance should be explained in this guy, but you do see very nicely that at some point we have a
couple of these principal components where you're able to just make a selection and it's all just kind of one class, right? So that's that's already
kind of cute. Now what I can do is I can say, well, let's use um instead. I'm just going to
zoom out for that part of the demo. So I'm still going to do eight components. What do you think might happen if I turn
on UMAP? Like how would this picture change, do [snorts] you think?
Uh, if I had to guess, I'm going to uh I mean, well, you are the guy that made the algorithm, so like I am [laughter]
curious to guess. Well, I I'm guessing the uh different classes are going to be a little more
clearly separated, right? Um, and what makes what makes you think
that? Oh, I've run this algorithm on this data set not to this number of dimensions but
uh okay let's have a look. So I'm going to turn on um mapap and it so one thing with um
is it takes a little bit to run right? So we can see but still it takes like four sec four seconds for like 2,000 of
these images and this is what it looks like now and this is almost like an art piece I think like it's very pronounced
right? Mhm. So one thing that's also kind of
interesting is what I find easier to do in this uh space is like suppose we just
select trousers. Now you can very clearly see it's like a very defined cluster that's happening and there's a
few things on the edges. So it's pretty easy to just go ahead and select some of the outliers with this technique. And
you can kind of see like okay that's most of the trousers are like straight but some of them have this Vshape and some of them are just thicker, right?
Yep. So, okay, like one thing I find UMAP to be a bit better for is just finding all
the weird outliers. But the other thing that I'm always just so surprised by, um, what I can do is I can just throw
away the label. Oh, and it needs to rerun. The UI needs to be improved, but um, I
can throw away the label. Uh, and what I can then do is I can say, you know what? Uh, let's just use, let's just pretend
that we don't have labels whatsoever. I'm just going to color one principal component here like the first dimension
basically. I'm just gonna and like even with no labels whatsoever, you can just very clearly see like the same pattern
still kind of emerges. So there's this red band over here that seems to go everywhere, right? I can still make a selection
and they're old trousers. Or I can go for this other band uh I don't know, yellow stuff.
These are mostly dresses. Maybe I can make a more bespoke selection. There you go. and somebody's dresses look a little
bit like shirts, right? But with zero labels, but you have something like UMAP and presumably uh something like this
parallel coordinate situation where it's just easier to make like a larger selection across all these different
axes. I mean bulk labeling is just so much better now, right? Yep.
So that so that's already I think like like good accomplishment on UMAP here, right? But this is just dimensionality
reduction. We're not really doing anything with clustering just yet, but this is like I think a really nice thing about UMAP. And again, I'm just going to
uh just for fun, let's just maybe increase the number of components. See if that actually matters.
Yeah, diminishing returns. That's what I expect here. It gets uh it gets a bit messy. That's
like one way to describe things, I think. And again, we can select this uh for the coloring.
And yeah, you can it's not the same as in PCA where like most of the variances in the first component like with a
mathematical guarantee. I think the order matters a bit less. It's more about the local clustering. [snorts]
Um but you it's not like I'm able it actually becomes a bit harder for me to pinpoint the clusters I might almost
say. So there's definitely a upper limit to what is pragmatic with the trick that I just
showed you. Um, before moving on, I'd like Have you seen this parallel coordinates thing u in real time before?
Uh, I have seen a little bit of stuff with parallel coordinates selections
like that. I haven't seen it used quite like this before. Okay, this is nice.
The So, it's definitely preview mode is the one thing I want to say. So, I have this library called Wiggly Stuff. This is one of the components in there. Um,
the whole point of wiggly stuff is I need to be able to show the utility and to demo it, but there's a few rough
edges here and there because JavaScript is not my biggest forte. Is there anything you would like me to try with
this now, though? Because I'm This is the first time I'm showing you a new toy, right? So, I can imagine that part of your mind is going like, "Oo,
Vincent, could you try this?" Just Yeah. Uh, so I mean, I I really like the
ability to pick out the outliers. That was nice. and is harder to do uh
outliers with regard to a given class, right? Like some something that clusters in one
dimension but then there are outliers with regard to the other dimensions. That's that's harder to do on the the
scatter plot style representations. Yeah, I can imagine. So the trick where I just select this
one class over here and you can very clearly see. Actually, this one's interesting because it seems like there's two classes like
there's two things in here, right? So there's Let me have a look. Well, exactly. Yeah. So, let's have a look. Um, so this
should be all t-shirts and tops. If I move this guy up,
okay, so it's like the white t-shirt and the darker t-shirt.
Yeah, they're still all t-shirts. And then if I make a selection here in
general, okay, it's not like this is a region where there's dark stuff, but uh Okay, okay, I agree the
Yeah. So those that's like a triang this is a triangular shaped sneaker. Yeah. Yeah. I mean they're they're weird
shaped shoes. It's not that surprising that especially I mean the trick is to remember it's it's working on the raw
pixel space, right? So yeah. Yeah. Yeah. So it's like Yeah. So like regions where all the pixels are
like super bright, that's going to overfit on that, not so much semantic information that's in there. And if you do this for I mean the cool thing for
the like for demo purposes, it's nice to show an image here. it's kind of hard to have like a bunch of sentences there and
then at a glance you can kind of go like oh these are sentences about this like you have to spend time reading all the sentences. Um
so so a a fun thing that we have uh built is a a library called uh toponomy
for for topic modeling style things just just focusing on the question of having an an LLM summarize topics.
I wonder if you could play a similar game and if it's just text have an LLM
provide a summary of what's what's common about the text and I guess
ideally for something like this uh what pieces of text are different or don't
fit the pattern. Yeah, the only downside there is the LLM will be slow like if I do this select
and like show thing here. Yeah, it's a
interesting question. Yeah. Well, I mean, so like it like it might be the case that it doesn't matter that much like waiting 30 seconds like
you know we we don't have to have everything within a few milliseconds, right? Um yeah, I I think you can get LLMs that'll
do it for you in uh maybe maybe a few seconds. I depends depends on the LM
but it doesn't need to be a a top tier model to be able to just provide a very simple description of what you're
looking at. Yeah. And also like it depends on what the document is. Like if every line here is just a sentence, that's different
than if it's a full paragraph and that's different than if it's like a full page. And um there's all sorts of nuance there.
That's true. And also you can do the sampling thing where you don't pass oh big selection. Well, let's not pass all of them to the LM. Let's just sample 20
and and do that. There's all sorts of things like that that you could do. That's definitely true. Yeah. uh we so so I I'll I'll give you
some insight into toponomy spends a lot of its time and effort in coming up with
smart sampling techniques and pre-summarization techniques like pulling out uh key phrases or other sort
of sub features to really distill down a prompt to hand
to the LLM. That's still I I think there's games like that you
could play. Uh that kind of gets beyond what's easy to code up for a a widget
like this, but maybe you can borrow code [laughter]
or five bit these days. Um well, I mean it is interesting that like one thing
I'm kind of curious how you see that. So do you also sometimes think that um because we've got all these LLMs now
that could sort of generate some of this code for us. I'm assuming that you vibe code on occasion, right? Just assume that
that um suddenly ideas become just a bit more precious. Yeah,
definitely. I mean, you can have lots of interesting ideas and ask the LLM to code it up. And I I mean, to be fair, uh
I'm much more in the research realm. So, I have, you know, crazy ideas and I ask the LLM to code it up and uh then try it
out and it doesn't work. And then I spend a bit more time and try and code it up myself carefully and it does work
but there's like it's subtlety and implementation. Yeah. Yeah. Well and also um one thing
that I've also recognized and it's like in a similar vein like you read a paper you kind of go oh that seems interesting. I want to see if this works
on my thing but then you read the paper twice and you kind of go like well there's 16 tricks in this [laughter]
paper. uh which one do I pick to apply to my problem and does that even work and and
suddenly you do notice that like having a good brain is still super useful. Yeah. I I mean it's also my ability to
explain to the LM what I wanted to code like if there's if there's subtleties and tricks that are required maybe my
ability to describe to it what I'm after is not so good. So yeah, it's it's it
subtleties go both ways. Yeah. Yeah. Yeah. the um I I probably don't have time to show that now, but we
do have this new thing in MIMO where it's called MIMO pair. It's a skill that lets the LM access every single
variable, but if you're using any widget, it can also actually do the UI thing for you. So if you have like
sliders in MIMO, the LM can actually set the slider values as well. Oh, that's nice.
Yes, that's um different demo. Very fancy. Gladly, we'll gladly show that later. Um but we we've got you on, so we
also want to zoom in a little bit more on the new algorithm. So, okay. Um, for those of you that are joining now, um,
basically what I've been showing Leland so far is, you know, we have a very fancy way to take something like UMAPAP
and to visualize it and, uh, we can show clusters very nicely. That's very useful with UMAP. So, you know, I could go here
and like, oh, there's a shirt that's like in the blue region. What's up with that? That's a very cool trick that we can do. Um, but now there's been some
new research and we can actually uh evoke and I put the E there for emphasis [laughter]
and it only now starts dawning on me. That was like the original plan to call it that. Um, but then I figured like we
do we can do the same trick but now besides just showing all these principal components, we can also add your new clustering algorithm and then we can
sort of play around and reason about what might be happening here. So that's what's happening down below.
So there's a slider over here that lets me set the approximate number of clusters and um I can sort of move that
around. That's like a a setting that I can pass to an algorithm. But the main thing that I did up front and I am
hoping that I didn't make any bugs in this is I have your new um algorithm to
put it bluntly. So, oh okay, there you go. So, the slider value is not actually in there. Um this is the new clustering
algorithm. So, I'm just going to go at it, you know, kind of point blank. We'll just see what we get if we use it. Um
we're going to take our data. We're going to add a new column that's going to be the fit predict that comes out of this clustering algorithm. important
detail is I think only fit predict is implemented. So you can't do fit and then predict. Fit predict is the the
main way to go, right? So it's not like you can fit on one data set, predict on another. It's like all in one go. Yeah,
if I'm not mistaken. And when I do that, I'm able to add this new cluster to the side over here. And one thing that's
pretty cute is I can actually um like you can see clusters appear on uh all
those principal components, but we can also see them appear here. And one thing that I just thought was pretty
interesting is you do have a big cluster for um like not like minus one, so like
not part of a detected cluster. But one thing is that if I were just now sort of scroll up and hit all these different um
clusters, then it does start to dawn on me that sequential clusters tend to be a little bit similar.
So cluster I believe uh what is that one is pretty similar to cluster two.
And then we hit cluster number three which is very similar to four. I mean there's differences but they seem to be
quite similar. Then we hit five which is similar again. Six 7
8 9. Okay. So there are some differences but it does seem that the sequence that we have in this clustering also says
something about the neighborhood that we are in. Um is this an accurate assessment of this clustering algorithm?
Depends a bit on the hyperparameters. I'm assuming it's like a thing that I'm noticing. I mean that's going to generally be true. It's I you can think
of it as a like tree based algorithm for clustering component. So they're going
to be sorted by depth in the tree. Sure. But like it's not not every
clustering algorithm has this property, right? Like if I do k means, then it's not going to be a guarantee that cluster
five and six are somewhat similar. But because something is happening here, it does make sense that clusters that are
approximate in number could also be approximate in their cluster. Yes. Yes, that is definitely something I
would expect. Right. So, so that's a cool thing to observe. There is another thing I would like to observe though and that is and
for that I actually need to be able to use this uh slider that I that I defined. So here I'm doing um you know
approximate number of clusters. Let's just use the slider value for that. Um,
and what I can just do is I can yeet this this direction. I can yeet it in this direction. And the main thing I would like to show is just notice how
near instantaneous this thing is. So unlike the UMAP thing that actually takes a little while before I can
actually see the thing update, I'm I'm almost of the impression that rendering this thing is computationally more
intensive than actually like the debounce rate of the slider is being
utilized is [laughter] the thing that I just want to observe like it's a near instantaneous clustering algorithm. And
what I can do is I can just maybe increase the number of samples to like 5,000. Um and again we can see that the
first um like parallel coordinates chart it's taking its sweet time because um
needs to run and um is famously not the quickest algorithm to run. But if I now go back down here again and I do the
swapping thing I mean sure it's a little bit slower but barely
and the first time that you run it I think is running Numba. So like the first time around it might be you know it needs to it needs to warm up but once
it's warm this thing is fast. It's like also I think a thing like a feature that people should not sleep on. We still
have the thing where cluster cluster numbers that are close to each other also have like similar shapes at least when I look at all these principal
components. Um but I believe uh this is like the the quick summary that I can
give of what seems to be happening in this algorithm and um I' I've also got some videos from you that we can also
discuss. But before I move on, is my approximate sort of first glance at
what's happening here accurate? Might be Yes. Yes, I I mean it's is very much
designed to be as fast as possible. So, um future future directions for this
algorithm are adding some options to manage uh to wait a little longer and
maybe get even better clusters. Um but there's a lot of work I need to do to make that happen. Um predict is also a
useful thing I would love to add. Uh and soft clustering. So these are all things that it does not have,
right? It would be nice to have and I at least have sketches of ideas for how that should work. But uh the the main
motivation here was that so many things these days are embedding vectors and
they're very high dimensional and the classical clustering algorithms do a poor job on them and I wanted
something that could run as fast as K means but do a good job. I mean historically I
do think like UMAP did pretty well and there are algorithms that I mean K means on UMAP is a bit hit or miss but um
there are clustering algorithms that do just benefit a whole lot more from just having the UMAP thing happen beforehand
but um for most of my use cases I've always just kind of found that when do you make clusters well it's to explore
the data a little bit and then things that should be close together but then one thing you also notice you can also just make this one sample around here
[laughter] and just use um Right. But then I did notice, oh, we now have a cluster
ringing algorithm that is also substantially quicker. And that was the thing that was sort of interesting to me. Um, because if even if you wanted to
use um as a pre-processing step, you're not going to be as fast as this. So that was also just uh like like was was speed
also the main interesting thing or was speed like a happy coincidence eventually?
No, speed was speed was the motivation. Okay. Okay. So speed was definitely the motivation in designing this thing. It's
also like yeah I I was I was trying to so I was
trying to design a clustering algorithm. I came up with a really what I felt was clever idea and I implemented that and
it was it was way faster than uh doing um and then HTB scan. It produced
slightly less good clusters. Uh so I was pretty happy with that. And then then I
had a thought, oh, I you know what, I could I could uh have some tricks that
would make the UMAP HTB scan combo run a little faster and then these would be more comparable. So I started
implementing those and uh and then the ball got rolling. [laughter] Yeah. Yeah. Turns out when you when you
um open up the hood on these algorithms and have familiarity with them and know
what corners you can cut where you can cut a lot of corners. I mean so but then the corner cutting
here was also because you knew like I'm just interested in the clustering. Therefore like a lot of stuff in the
middle that people might want to have because they want the full embedding. If we just don't allow people to access that then clustering becomes a whole lot
quicker because there's all these shortcuts. That's kind of the yeah the thing that happens the guts of it. And also uh just because I'm cheeky,
I got to ask um were were LLMs useful in the in sort of designing this or was it
still kind of I don't know like when was this was this GPD claw 3.7 era or was it a little bit
later? Probably most of the work was done in the like 3.7 era. Oh, right. So, okay. It was also it's
been a while. Um do you find yourself using LMS a lot when you're researching or is it just still prototyping more?
Um actually I like having conversations with LLM about research ideas. I mean I
don't always have good uh good answers but uh
it's not I view it as a Socratic dialogue. Yeah. Yeah. Socratic is the key word.
[laughter] I'm looking I'm looking for them to say something that will make me question what I'm what I'm doing and and then
work from there. It's Yeah. It's it's it's just uh I mean it's almost like uh rubber duck debugging if you're familiar
with that. Yeah. Yeah. Know and also like it sounds weird but one thing I found incredibly useful is sometimes the response is just
so bad that it makes your mind want to go completely orthogonal to what the LM just told oh that's a useful direction.
[laughter] Exactly. Yes. Yes. Um it's not it's not it's not for getting answers. It's for asking questions.
Yeah. You with with Oh, why did you say that? uh let me let me rethink what I'm
I mean even just as I said explaining how an algorithm works or how how uh an approach is going
to work if it doesn't understand it and goes off on some tangent well okay now I
need to think about how I'm explaining this yeah it is a nice mirror in that sense
of like oh if I can't explain it well maybe my thoughts aren't aligned as as much as I would like to think
the the one thing I did notice though and it's like yeah tangent. We're going to come back
to the algorithm a bit but I think you're going to sort of enjoy the story. Uh I was playing around with unit
spheres in high dimensions because I made this parallel coordinates thing and then you want to you know have examples that are tangible. Turns out this is
actually a terrible way to visualize a unit sphere. [laughter] It works for a lot of things. Doesn't work for unit spheres. But then I
figured, okay, I should I should ask the LM, can you make me a simulation of like a unit sphere in high dimension? Because
it's a nice simulation to show that like the angles on a unit sphere, they kind of approximate a 90 degree angle when
the dimension becomes very big. It's like fun little math proof. And I saw it implement a thing. I was
just so furated because the implementation was literally, okay, we're going to have a for loop numpy
array. Numpy array, we compare the two numpy arrays. both numpy arrays were random. But you
do kind of go like okay but a unit sphere is um rotation invariant
your code should use that fact. [laughter] Yeah. And it didn't. And I immediately kind of went like why would you implement it
this way? And then also you don't have to generate two full numpy arrays. You can also just generate one big numpy
array and then slice in the for loop to make sure you don't allocate memory needlessly. And you do kind of go like
oh but maybe I should have also added that into the prompt somehow and not asked it. [laughter]
like a blunt implementation because in the end it was doing what I asked it to. Um it's just that oh I don't notice how
bad my question is until I actually see the result that it ends up with. [snorts] Uh very emotional conversation with the
LLM there, [laughter] but but I I can imagine you can sympathize. Anyway, um you also um sent
me two videos that can help explain what's happening under the hood cap here, and I think they're they're good to maybe talk about. Which video should
I show first maybe? And one thing also I can pause and um there's one video that's like a minute long and there's
one video that's like 30 seconds long. Which one do you think might be good to start with? Oh uh I I think the overview is probably
the place to start uh as one as one imagines over as the overview word implies. This might give
us Yeah. Yeah. This is this is like a sketch of uh the guts of what's going on. So it's the basic process is we
start with embeddings because that's what we have and we want to move down to
this this manifold. So we're doing some sort of manifold learning. Then we want to do some sort of density estimation.
And then we want to pick out multiscale clusters out of that. So that's the
whole process. Okay. And the whole and then individually within that you can you can pick out what those
individual pieces that I'm gluing together into that pipeline are are like. But that's that's the guts of the
process. So I would be interested if we can explore the multiscale clustering aspect which you didn't have in your
your interactive demo. I have you have you played with that at all? Not so much and it's mostly due to uh my
even I have a kid now so the evenings are a little bit more time time is time is hard to come by. Yes. But one but just to make I just
want to make sure that I understand like the full picture. So this is the step that some people like to call embed. So
typically like this could be very high dimensional when we say manifold typically that means go into a lower
dimension. Yeah. Could it also like that's usually what we're talking about here. Can we come up with some sort of representation that's
lower in dimension but still contains as much information as possible for most tasks.
Um yes. Okay. I mean uh one way to think about this is that uh for the next step we really want
to do some sort of density based clustering. And it turns out that in high dimensions uh density just doesn't
really exist uh in the sense that you need exponentially more data.
I was there curse of dimensionality right there. Right. Yes. You're just you're just not going
to see density in high dimensions. But there's if there's actually structure there
uh you can pull that out and then if you collapse that down to a low low enough set of dimensions now your density
clustering can actually start to get traction. So that manifold step is
basically trying to extract out structure from the highdimensional data and put it in a place that the density
clustering has traction. Okay. And then and then also the thing with and one I can smell this. I don't
know if it's actually going to be the thing, but one thing you can kind of imagine, oh, there's like a big chunk of uh density probability mass over here.
Oh, that's super useful. And then within that chunk, there might be two other chunks. And that's kind of where this
hierarchical thing might come from. Or am I skipping a step? Nope, that's that's exactly it. So the the multiscale clusters is uh a newer
newer technique. Uh it was actually uh developed by uh Gelmerbot who is uh very
good at this sort of thing and it it is a cluster extraction technique for
things like HTB scan and that's what the second video is about is is going into the details of how that one actually
works. Should I uh go back to the notebook or should I press play to finish this video at this point? Let's uh uh notebook. Yeah, let's let's
let's let's play with the uh cluster layers if we can. Yeah. Okay. So, we I've got this
estimator thing over here, right? So, let's just make a new cell. Uh here's the estimator guy. Oh,
fancy keyboard shortcuts. We get we get this uh all these fancy things that are in there. Um but I'm assuming we're
going to use a we're going to call a method now, right? Uh, no. As long as you fit it
then, uh, oh, see, now I'm trying to remember my own parameters. [laughter]
I think I think it's cluster layers. Okay. So, what another fancy feature uh
inspect uh so we can inspect this guy and we can say something like methods
equals true and then we should see
cluster layers. That's what we want. cluster layers underscore. Oh, okay. So, that's one of those estimated properties. Okay. So,
yeah. Yeah. Yeah.
Underscore at the end because we are in psyched learn. [snorts] Okay. Okay. We So here we just have one
because you asked for an approx number of clusters. So if we were to rebuild
the estimator without that. So without that so this we can just throw this away,
right? Yep. even list parameters. Want to throw away number of neighbors, too? H may as well. Let's let's let's try it
with nothing. Uh oh, and and but let's actually do assignment to a variable. Yes, that
would be good. Oh, it took longer now. Is that because that's because the number had to heat
up, I think, right? Probably. If you run it again now, it's a bunch quicker. Okay. Yeah.
Okay. So, that's so that makes some sense. I can imagine that like given some hyperparameters you may be able to
in okay that's number detail we'll think about that later but hey we see four things now
yes and so the each of those is a set of
labels uh the same as you had before for clusters
but they are at different resolutions. So you said I want approximately 30
clusters. This is uh telling the algorithm I don't I don't care. I I'll
I'll take a really fine grain layer. That's layer zero. And you notice there's a 119 there. So there's at least
that number seems bigger than the biggest number I see over here. Yeah. And so as you go down in that list, you're getting uh different
cluster resolutions, but it's trying to naturally pick cluster resolutions that
will work. So just to confirm uh that number phenomenon, right? Uh list
objects has no attribute. Um I thought this was a dictionary, wasn't
it? Yeah. No, it's just a list. Just a list. Uh but you
hang on. Oh, it's a list. Okay, never mind. Enumerate is then my friend.
Enumerate because I am a little bit curious about just the scale there.
Yeah. Okay. So, only 12 all the way up until a bit much bigger number. So, that's uh okay. Confirmed. Very good.
And then do we also are we able to access this information
per data point as well? that each each one is a label per data point.
Oh, so this is as long as the number of predictions. Yep. Ah, right. Okay. So,
you can pick any one of those layers and plug it into your parallel coordinates plot.
Or I I would say plug them all in as extra dimensions.
Oo, like where this ship is sailing. Um, we are going to have to write a little bit of Polar's code in order to do that
though. Okay. So, um that's okay. So, we're going to call whenever I have a data frame that's
meant for plotting, I call it plotter. Um and we are just going to do this manually. So, we are quick and dirty
about it. Let's remove opening bracket there. Plotter can go in. So, we already
did the uh that guy. And at this point, we've got cluster layers
with an underscore. And we can do zero. So, we can call this C0.
Uh, we can do that. Okay. Um,
and this is the point in time where I show like a stupidly simple but fancy shortcut. I can highlight the zero, hit
command D, and put one in there. And I can highlight this, command D, and I can
put a two in there. And I can also press down now and put a three in there.
Uh, there we go. Oh, this is fun. Um, but see, uh,
but of course, if we rerun this, uh, we might actually, it is randomized, it
seems. So, we might get four or we might get three. Yeah. Yeah. Just a just a thing to be
aware of. No biggie, but like um you can set a random seed, random state
equals 42, and uh all will be well. That would be uh the way the world usually moves, right? Never go for 41.
H. Oh yeah. Uh because psychic learn convention. Yes. Uh we have four.
So that means I could put this guy back and I can do my fancy trick with the keyboard shortcut one more time. Make
the selection. Command D and three. Oh yes. Run again. Okay. So just so we
agree. So zero was the highest fidelity thing. And that also makes sense. If I make a selection here, you can see it
sort of branch out and branch out. um we still yeah and this sort of goes
all over the place but this also helps explain why at the lowest level because I think when um this is the stuff that
the algorithm puts out right like this is the final clustering um so it makes sense that
things are similar because again we have the hierarchy I so so in fact uh the if you just do
fit predict and ask for the label ask for the labels it will output whichever
layer it thinks is the best layer Ah, so there's some extra intelligence happening.
So, so C 0 is the finest grained clustering
that it's going to do. It might be too fine or like the algorithm there's a there's a system in there that can determine well this is
too fine. We need coarser sand otherwise we have we don't have rocks something. Yeah. Yeah. Yeah. It tries to choose the
optimal resolution as the single output clustering. So
okay that's I mean but you can also approach that manually which is uh definitely cool but also um this also
confirms that you cannot do this trick unless you do fit predict. Yeah.
Uh otherwise you get into scikitlearn wants to predict multi-dimensional output territory which is bit of a
rabbit's nest but uh good good to know. One thing it is interesting to see is you do see the
Yeah. Yeah. So it is okay. There's there's relatedness in
Yeah. the the classes like blue and purple the light blue and purple seem to go
together for reasons that I I don't know what those classes are.
Well, but thanks to the power of parallel coordinates, we can just [laughter] check. Let me hide the code there.
Command H. Move this guy up. We can just have a selection. Yeah. So, apparently there are t-shirts that look like
dresses because they're like sleeveless tops, right? Makes sense. Makes sense. Let's get a little bit of
red in there. Uh, and these are also dresses, but these are fancy ones. And let's go. So, that's also red. Maybe
something in the middle. Yeah, this is like dress territory plus stuff that looks like dresses. We also have a blue
territory here where we've got shirts. Uh yeah, that's a bit annoying. So there's
shirts and there's t-shirts. Yeah. Yeah. Which I and a pixel label look pretty
similar, but Yeah. And and like but but like from a Vincent is not really that fashionable
perspective. It's like same difference, but anyway, that's a different [laughter] that's a discussion I usually have with my wife. Um but okay, but this is
definitely cool. Not a lot of algorithms have this hierarchical lever. Uh is this the point in time when I should go back
to the video? Yeah, I mean the we can talk about basically how it's how it's doing this
because it's it's not a standard treebased approach. So yeah.
Oh but is one the video suggests that you're using um youap here. I like partially true.
It is uh it is a very custom. Right. Right. Right. Right. Okay. No
like tweaked and and I see HTB scan here. That's also probably HTB scan like
exactly a bunch of custom knobs tweaked. Yes. And so PLC scan is is uh Gelmer's uh
variation on on this uh and I because I I was working with him on that. I I just
uh said that's too good an idea not to use. So and his name was Yammer B. Yeah. I
that's a Can I say that's a Dutch name? I honestly don't know.
Okay. Well, it sounds Dutch. something for that. It may well be. Okay. Um I'm obliged by the Dutch
government to mention if a name sounds Dutch. Of course. Yes. Um but okay. So you are So this is
definitely a Okay. So maybe I'm going to phrase this a bit bluntly. Part of the innovation here is reusing old tricks
and realizing that when you chain them together in a pipeline, you can optimize things. Yes. Yes. Very much. So it's it's all
the things that probably many people are already doing. I think the UMAP and the HTB scan combo is popular for embedding
vectors. Yeah. Um but you know if you're just
doing clustering uh turns out there's a lot of a lot of shortcuts that you can
make and you can also so I I will say uh the
effective loss functions in the version of um here are very different than than
um there they've been um to enforce more clustering
If you were to Okay, so um I recognize so we could we could go for the video but maybe there's like a one sentence
answer. If you were to summarize like what's the main insight that led to like speed up and progress like how would you
describe it? I don't and if we need to use a lot of math we can skip this question for now but just out of curiosity if there is a simple answer it
would be nice to know. Uh I the the simple answer is that in the end UMAP
actually does a lot of a lot of late work in the optimization procedure that does a great job at fine-tuning things
for visual representation. Oh right okay but then I on one okay but then the observation might be as simple
as visualization is very much a non-discrete thing.
Yeah. Clusters need to be visual and like all of that clustering very much is yes or no in cluster. Therefore, there's
nothing in between. So, that space can be removed. Very handwavy, but that doesn't Yeah. Yeah. And so, there's a bunch of a
bunch of tricks you can do to help uh encourage that to happen. Sure. And something is telling me that
this video might give us a bit of a hint. Uh uh this is this is all about the cluster selection. So,
okay. So, an H HTB scan can output you can think of this as like the condensed tree in HTB scan.
Okay. And so if you if you hit play, you can think about HTTP scan. You pick out
leaf clusters sometimes and if you vary them in cluster size, you get different
leaf clusters being picked out. Mhm. Here we're just waving that around and the gold is the cluster that's selected.
So if you pick the right minimum cluster size, you get clusters you want. Fancy animation, I got to say, by the
way. Well done. Um, so what we can do is just start
varying the min cluster size. And I'm going to start a bar whenever a cluster
gets picked out and end the bar whenever that cluster is no longer valid. And so
now we get this barcode. This is like persistent homology. And you can actually write this in terms of persistent homology. But then you go
through and you're going to score each minimum cluster size by the total
length of bars that exist at that min cluster size. And so now I have this
score for each possible minimum cluster size. And there'll be a maximal persistent score that's going to be the
the cluster resolution that it will pick out by default to use. And all the other
local maxima in that plot are the alternative cluster layer resolutions.
So that's how we get these cluster layers. Okay. But okay. Okay. But but it's a okay but it is a local maxima that and
and I can also imagine if you set the seed differently this shape will be a bit differently there for all these
local. Yeah. Yeah. So you'll get a different number of
layers if you if you haven't fixed the seed because there's there's randomness in the uh dimension reduction step is
probably the best way to put it. Okay. So I have to admit like it's it's been a while since I since I did the how
does this algorithm work again like full explainer in depth but and also maybe for the audience we're going to attempt to see if we can make this as intuitive
as possible within like a minute or two. Yeah, we might not be able to but we'll see. Okay. So what is the point index on the
x- axis here? Okay. So this you can think of this as
uh HTB scan works by building a minimum
spanning tree. Yep. And then uh you turn that into a a like full cluster hierarchy. It looks a lot
like single linkage clustering where you get your your dendrogram, right? So but you start at the point you
say connect this to the nearest neighbor. You do that for all the different points and eventually you get this giant tree. You get a giant tree.
Yeah. Uh so you can think of this uh this plot as uh laying out that tree. So
the the the point index is sorting according to uh relative depth in that
tree. So and where does the tree start? Starts at the bottom. So the root of the tree is the bottom that has all the
points one cluster. Okay. And then like you go inward one step and then you go inward one step and
you go inward and inward and inward and eventually you hit the center. Yeah. And so singleton points are just
getting discarded and and and that's all we're doing here, right? And and once you discard the
first layer of singleton points, you get the next layer of singleton points, but you go inward and inward and inward and
then eventually I mean so that's also what we see here, right? Like data gets thrown away, gets thrown away, gets thrown away, but at some point you're
going to get the minimum span spanning tree. It might actually start to disconnect. Or is that not what's happening here?
That's that's essentially what's what's happening here. So this is this is the dendrogram except I'm not drawing any
connections to anything that that results in a single point or in fact for this one I think there's a a base
minimum cluster size. So any cluster that splits off that's below a a small
enough number of points instead of drawing that in the diagram is just going to throw it away. So as the
minimum spanning tree splits into components, if any component is too small,
I'm just going to drop it from the diagram. So we always get smaller and smaller numbers of of of points as we
move upward through this plot. Yeah. So this is one of those moments where Vincent goes, "What if I just draw
a random tree? Can I can I can I can I make this look the way I think it might?" And then you do get this awkward
thing where well, if you're going to start at the edge, right, and we're going to remove points, then you
typically get this thing where where we're going to cut these off first, right? Yeah.
And that makes some sense. But then this is still all one cluster.
Yes. Yes. So, uh, if you were to
have a a break in that tree that was going to split it into two components.
Uh, yes. So, so the main question, what shape does the tree have when that happens is kind of what I'm wondering.
So, you could look at this sort of tree and say like, oh, there's two clusters, but if we go from the outside in, we're
never going to cut this. Uh, so we're not working outside in, we're working by uh edge weight or
basically some sort of density estimate. So, eventually we're going to cut that. Okay. So, per node you just have a score basically.
Yeah. This one just have two connections and this one would just have two connections. Therefore, it's still a pretty low score. And then if you have
like a giant cluster of stuff over here, um maybe these two points would also have a low uh connection, but these
wouldn't. And then you can still get these clusters basically. We're still going to get clusters out. We're eventually going to to have a cut
like that. And that's where you see the actual clusters starting to appear in in the plot,
right? But when I said outside in, you shouldn't think of it as leaves that we're going to and then move inward. No,
you should think about some sort of connectiveness and then that's how we're going to prune the tree. Yeah. Yeah. We're going to prune edges
and that will split off components and some of those components will just be small components, singletons or or
otherwise. Sometimes it'll split into bigger components and that's where you see the clusters in this in this plot.
Right. Right. And then and then estimated density is a function on top of that. But by the time this could be
any number this is just a way of calculating the density but you can imagine okay given that we've got this layout now then we can again fancy
animation got to give credit where credit is due. And then you can do things like this where you can sort of say like okay but there if you then
define some sort of minimum cluster size that's basically an exercise of sort of putting a line down from top to bottom and then and then making a cut
somewhere. Yeah. Yeah. Okay. Cool. So okay. So that that that
definitely feel okay. Then we get to this bit and then you get the minimum cluster size and this is if you if you
sort of turn that slider into a verb and then over time you measure that's how you can get these lines and then you
sort of do the trick of like okay but uh you've got this persistent score I guess that's the one thing that then remains a
little bit mysterious what is persistent what's the y-axis in this case then uh so I think the easiest way to think
of it is uh that line the vertical line is crossing some number of bars they're highlighted in gold um sum up the total
length of those bars, right? Okay. And that's your score. Um it's a it's a
little there's some slight tweaks to that, but that's good enough to [laughter]
I do topology during the day. At night, I get to do the hand wavy things. Okay, joke. But uh Okay, but okay, this is a
little bit of a heristic then. Would that be fair to say? um or is there some mathematical motivation
behind this as well? So no there's there's there's mathematical motivation behind this. You
can think of this as uh so HTB scan is density based clustering
and you can you can do it to produce a flat clustering or you can do it to produce a a tree,
right? But you [clears throat] then need some means to turn that tree into a flat clustering.
If you want to do scale space clustering rather than density based clustering
in other words look at different resolutions then this is the actually mathematically
motivated way of doing that by using the density based tree to inform your scale
space clustering. So it's it's actually doing uh persistent homology over scale
space based on the tree. Right. So there is this actually real math behind this.
Yeah. Know so but it does sound like okay so the yes if you were to approach this from a very much uristic point of
view you would still end up with something useful but it also just so happens to be the case if you take the
oh we got to figure out what the function is that we got to optimize and we do the math properly then you would also land here like that correct and you
probably did path number two [laughter] in order to get here as opposed to path number one. But um but okay but but it
that does then start to make sense that we see the clusters that we see again because of this local optima observation. Um I guess like the final
thing just for and this is like a personal intuition thing along the way. I mean there's there just like a normal
research paper there's probably like 10 tricks that you're that you're applying here but I can definitely imagine that
if in the end the only thing you care about are these points in the middle like these points at the end. Let me put
it that way. um then there's a whole lot less that you need in the middle
like as far as the UMAP uh sort of uh goes because the only thing you care about is that you're able to come up with a resolution uh in this space so
that you can pick these four arrows. Yeah. So so so the um step becomes a lot
cheaper. Uh yeah that's that's that's a big chunk of
the speed up right. So is so the the heavy lifting is happening in this first arc. uh is kind
of what I'm hearing then. Uh yeah. Yeah, there's a lot of heavy lifting there, but I mean it's also
reusing tricks we already know, right? So, you know, if if if you're a person
that uh uses um and HTB scan to do your your embedding clustering,
this is doing the same thing. It's just doing it faster and better. Well, I mean, you don't get the manifold. That's like one thing uh that
you don't get, right? There's no visualization you're going to get out of this, right? So the so the I mean one thing I
could do I guess so part of me was wondering to what extent is my old school trick of like oh
we're actually going to do this uh parallel coordinates thing and we're going to use that to find clusters. It does feel like actually using um for
this is still pretty valid because you get these outliers to appear quite nicely, right? Um but you do have these other moments
where you just kind of go like okay let me just sample from this one cluster and maybe things should be similar. um like
it is a different use case using similar tricks but it's also safe to say it's not like this is going to fully replace
UMAP but we do have a new UAP. No, it's it's it's not it has no
visualization component. So it's it's not going to replace that. Uh but if what you want at the end of the day is
clustering, um this is a much faster way to get there. And the cluster selection
procedure uh that spits out these layers has some knobs to it. Yeah.
Yeah. Uh so I I've basically completely converted over to to this uh methodology
with the layers because I used to look at cluster trees in HTB scan and and
single linkage clustering and they're so complicated and so noisy and trying to figure out where I should be cutting it
is hard. Mhm. There's four layers to look through here. uh it doesn't take that long to to
glance through when you've got visualization tools like this and go, "Oh, yeah, this is the cluster
resolution I want." Yeah. So, it's it's pretty normal to have like a I mean, you have some variance because we just saw three and
four, but you're not going to get 16 unless something unless there's a reason for it. Yeah. No, it will produce as many layers
as it needs and mostly that will be a smalish number. Uh it's usually in the
order of like a a couple to 10 and that's
and it's still up to you things to look through. Yeah. Yeah. And it's still up to you as the user to sort of say, well, I just
can I just do high over now, please? And it's up to you to sort of say, well, let's just look at the second level and not bother with layer 10. We can do that
later. Um yeah. Yep. Is there like a a use case that you've seen or heard of where um
because I remember like I remember talking to you I think it was like a year or two ago where we discussed like what were some uncommon use cases of
UMAP and then apparently there's like art conventions [laughter] in like the the Royal Academy of New
York or something like that. That was kind of a unexpected surprise. Like I know that evoke is early so I can
definitely imagine that not every story is collected yet but have you heard stories from the field where people kind of go like oh actually like this one
technique works really well or surprisingly well for this use case that I've got or is it like early days? Uh it's still early days for this.
So so all you artists out there looking to get into the the New York Museum, pay attention. Um [laughter]
um but but but I mean the one thing I can confirm is it is surprisingly quick
and it is also like with this visualization I also find it pretty easy to confirm that you do get clusters that
seem very reasonable. If you if I cross reference it to the UMAP stuff I don't see anything that stands out as like
shouldn't shouldn't shouldn't work this way or something like that. It all feels like pretty normal uh just good clusters
verified via um that's what I seem to see. Yeah, I I would say that that that's
fair. It's uh it's I would call it exploratory clustering because
I it's designed to be fast. It's designed to spit you out a bunch of resolutions of clustering that you can
quickly have a browse through and see if this is categorizing your data in a
useful way. Yeah. And I can I can also imagine like if only as a pre-processing technique,
one thing you can always do is say, "Okay, clustering super quick." Oh, this cluster is now smaller data and we can
do UAP on this. Right. Exactly. Exactly. Just it's a it's a a quick and easy way to weed weed through
data uh fairly efficiently. Right. Okay. Makes sense. I am interested like Okay, so we're in
cluster eight here. We're looking at all the t-shirts. Okay, that's interesting. I'm going to look at all the normal
shirts and dresses. Yeah, I mean eventually a hard part with
a lot of this clustering and um stuff is also like what's in the embedding.
Yeah. So, this is just plain pixel values. So, it might just be a very boring well there's a bunch of black
there. That's why it's the same cluster. There's no semantic meaning or anything like that. Um,
is there any um I mean research papers are being written right now I'm assuming but
it's not like oh sentence embeddings works better here than like visual embeddings like a a lot of how good the
clustering is is still in the eye of the embedding. I think is safe to say. Yes. Yes. I mean it's down to the
quality of that initial like sentence embedding or clip embedding or whatever
embedding method you're using. That's cuz that's doing the heavy lifting of getting you from your raw unstructured
data to something you can actually work with. Mhm. How good that puts similar things
together, that's that's up to to that. And so evoke is designed for ah
presuming I've got that turn that into a bunch of like discrete categories
that I can work with. Does um does it also support discrete data
as in sparse data? [clears throat] No. Okay. Okay. So that's the one thing
that's fine. Um but but that does suggest that a lot of the motivation here really is the fact that the world
seems to be moving towards the dense embeddings for pretty much everything. Correct. Yeah. Yeah. I mean I still love my sparse data. I
mean to be clear I think it's a very useful tool. Um but it is interesting to
at least hear that the motivation does come from there. Yeah, I I just saw enough people uh
using this kind of pipeline of um HTB scan on embedding vectors
um that once I realized, oh wait, I could just make that a whole lot faster.
Um I I felt like that was a a worthwhile effort to just you felt obligated.
Yeah. I and also it's one of those things where you don't you don't think about it at all and then and then you
you realize oh I can do this and then you're like why has nobody done this yet? Um
I I admit to being disappointed that this didn't already exist and somebody else hadn't already implemented it for
me. It's funny you mentioned that because that feeling is exactly how this widget came to be. [laughter]
It's kind of it seems like so useful. I want to be able to do more than two dimensions. We have a technique for it. I'm not that great at JavaScript but
fine I'll figure out a way. Um and and again like for understanding this
algorithm I also find it to be so invaluable. Um because you can just very clearly oh yeah this is hierarchical.
You can just very clearly see that and you could kind of see that with two dimensions as well but having just more.
Yeah I I I love this as being able to add the multiple layers on that's the
the cluster layers. I hadn't thought to do that because I was trying to layer
them over say a UMAP visualization. Well, that's that's hard. Yeah, that is hard. I mean, that's
something you also learn when playing with like two dimensions. Um, there's a lot of information that you got to cram
in there if [laughter] you want to make it useful. Um, one thing I do want to do very quickly since we're we're close to
time, but what happens if I turn it back to PCA? It becomes brown, doesn't it?
Yeah. Yeah. Oh, interesting. Um, I'm using paint
metaphors now because we do a lot of finger paint with the kid and no matter what colors you start with, you always
end up with beige by the end of the drawing session. Uh, and it seems that uh
Yeah. So, okay. So, PCA is kind of the childish way of doing it. UMAP is the uh
more keeping the colors intact way of doing it. That's also kind of Yeah. I but I mean I hopefully that also
emphasizes uh how pure the colors are on the left hand side under the clusters.
Yeah, true. I mean there's some overlap in some instances, right? There's a bit of brown in there, but a lot of it is relatively pure colors. So
yeah, and I guess like that's this is the awkward thing with parallel coal or coordinates, I got to say. So it's one of the reasons why the colors here are
so clear is because there's between these two bars there's a lot of orange in between. Yeah. I almost feel like we got to add
some jitter [laughter] to really make that arc sort of stand out because a lot of lines with the
exact same coordinates don't shine as bright. Yeah. Um something I might think about. I mean
we could let's maybe do that at the fi the final thing over here because I think one thing I could do
is do something like nprandom.random and then I got to do uh shape or this is
a list right? Uh, no, no, that one's a vector. Um, vectors,
right? Okay. So, then I can do shape uh zero. That ought to do it. I think I can
see if we can add a little bit of jitter festivities and once again show off the cool keyboard shortcut.
Oh, very nice. There you go. Uh, pretty spot on.
Yep. [snorts] Yep. Oh, actually I actually kind of dig this
for cluster visualization actually. It does make the band like way more clear, doesn't it? It does.
Maybe. Yeah, let's maybe just [laughter] again all you artists pay attention. Um
but oh wait, hang on. So divide that by two. Just add like a little like maybe you still want to see the line, right?
[snorts] Just to make it clear that it's not all one cluster. Yeah. Divide by 1.2. two.
Yeah, this feels This feels ideal to me. The one thing that's a little bit Yeah.
Yeah. Because we're adding the noise here as well, it gets a little bit But you can still see like at least on this level, you can still see there's like a
gap, right? Yeah, that feels that feels useful. Um,
cool. Okay. Yeah, that's okay. Okay. I do think that's a nice cherry on top at the end there. That's definitely kind of
a nice thing. Um, okay. So, there are actually some questions people are asking in the chat and we can stick
around for like a little bit longer assuming Leland you you've got the time because I do think um someone is asking
like how does EVOC compare to Matrushka embeddings in terms of maintaining representation.
Ah, I mean it's a very very coarse uh
representation because it's it's turning things into just uh
a pure cluster representation. So I think it's going to be very coarse
compared to Matroska embeddings. And the other thing that I I think is being hidden a little bit in your parallel
coordinates plot is that minus one cluster which is the one I mean this guy is beige. Yeah. [laughter]
Uh I mean that is actually cool to see that this is actually pretty gray and beige. Uh
yeah it it doesn't cluster lots of points.
Yeah. Um which is either a pro or a con depending on what you're trying to achieve. If you want metroska style
embeddings um you've [clears throat] just assigned a whole lot of stuff to a class that
just is not in any way meaningful. I am super happy the question came in though
um from the point of view of uh somebody trying to categorize your data all our
clusters are mostly pretty pure and anything that isn't easy to categorize just gets tossed in that last bin and
there's a lot of stuff in fashion mnest that's actually surprisingly hard to categorize
and and also like one thing there's like one feature I forgot to show like I can make a selection here and you also see how many data points we've selected it's
like 12.4 for but the thing I can also do if I wanted to is I can say I'll just keep that
and then it's going to throw away everything except the thing I've selected right I can also restore and I I also just
kind of like the animation I can also just exclude like I can also do this thing where I oh let's just go for this uh keep
like a thing you can do and that also has the widget selection also respects everything that we're doing there anyway
uh cool to see and like one that is also a thing I forgot to meion Another thing that I did notice which I do think is important a substantial amount of uh
data does go into the minus one bucket 10% easy maybe more
definitely it it can be very high for some data sets um if if it's hard to
pick out because the goal here is to pick out meaningful pure clusters where possible
and [clears throat] again like the the color band suggests that we're getting there. Yes.
Um, so when it does cluster, those clusters are generally pretty good, but
that maybe at the price of having to throw away a lot of data. Um, which is
which maybe that that bucket is an interesting one to go through in that that's hard to categorize things at
least automatically. So those are things your embedding vectors struggle with. So let me try. So what I there there's a
bit of brown here. Let me try to see if I can select a brown uh in this region as well because there's some blue over here that's like still pretty good but
like okay let's go for some brown here
I mean again pixel value that's the downside of is pixel values right so
yeah it's hard to do the most conclusive thing with this because of the data set but I I [clears throat] do agree that
like looking at outliers tends to be a good pastime people will underestimate uh how much you learn from understanding your outliers
Um, cool. Um, anything [clears throat] else worth of sharing? Because I mean there's
like an audience of people that are going to watch this. Is there any feedback you would like to get from people giving this a spin? Is there
anything you would like people to try? Is there anything that makes you kind of go like oo um I would like to see more
of this. Well, I I'm actually honestly interested in how the the cluster layer approach
works for people and apparently it is not discoverable enough because uh you hadn't uh played with it yet.
Um I mean I did I did touch it. I just didn't have the intuition of what those numbers exactly meant and I was
Yeah, I I I feel like it's a much more powerful way to explore
than a tree. like trees are a lot of work to dig through. Uh a small number
of layers of different resolutions make it much easier for you to quickly dig
down and go, "Oh, I yeah, this is too fine grained or I I need a little a little more detail than that." And you
can even do it on split out one cluster into its lower layer components.
like you rotate your head a little bit and they you actually kind of see a tree with like different colors of roots.
Yes. That's actually kind of a cool thing here too. Uh [clears throat]
yep. Okay. Awesome. Now, so um what [clears throat] I'm going to do is I am going to take this example and I'm going
to put it on the So Mimo has this very fancy gallery and I'm just going to put it here. Like I have I have the standard
MNEST parallel coordinates demo, but I do like I um the fact that we have this
part sort of missing. I I think this is definitely like a core semi semi- crucial thing that people should maybe
appreciate a bit more especially because the way that this parallel coordinate is is designed is it can't actually handle millions of points. It's going to be
hard to show because it's not a big data set. But um you do notice that if I were to click away just very briefly, you can
see that the lines are actually being drawn in real time. So on the front end there's this one select like uh this one
widget that allows me to make a selection. Once a selection is made the canvas element in the background starts drawing lines and it's doing that
continuously. It's actually streaming those lines in and that way actually can show every single line but it's not
going to have everything rendered to the DOM. So therefore the browser doesn't collapse. [laughter]
So there there's some tricks you got to do in order to visualize this nicely. And the library on the hood that I'm using for this is actually really good
at that. So, a small little extra detail. Cool. Okay. Um, I'm super happy
we had this talk. Um, so thanks for being the first in our new round of live streams. This is definitely people were
super enthusiastic, not just in our Discord, but also on Reddit uh to have you on. So, there's definitely people
who are doing things with embeddings and would love to hear what quote unquote Mr. UMAP [laughter]
is exploring in this domain. It is your claim to fame, Leland. I'm sorry.
I'll take it. But super cool. Yep. I I I feel like there's a lot of
opportunity for this to uh find some use. So, I'm I'm keen to see what people
people do with it. Especially, as I say, I think the the layering is nice and it would be good to get feedback on how
useful that is in practice for people. Super. Um people can find you on most of
the socials and if not, you're still on GitHub, I think. Right. That's correct. Cool. Then virtually I'm sure people are
applauding right now on the normal conference be the point in time where I um you know thank you once again that I can do but doing a full applause on
behalf of the audience is a little bit hard with a mic but thanks for dropping by and this is the point in time where I'm going to hit stop on the stream
button.
