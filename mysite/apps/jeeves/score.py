from collections import Counter


class ThreadScore:
    def __init__(self, users, posts):
        self.users = users
        self.posts = posts

    @property
    def posts_per_user(self):
        return dict(Counter(self.users))

    @property
    def words_per_post(self):
        return [self.words_in_post(p) for p in self.posts]

    @staticmethod
    def words_in_post(post):
        return len(post.split())

    @property
    def words_per_user(self):
        wpu = {}
        for user in set(self.users):
            indices = [i for i, x in enumerate(self.users) if x==user]
            user_posts = [self.posts[i] for i in indices]
            user_counts = [self.words_in_post(p) for p in user_posts]
            wpu[user] = sum(user_counts)
        return wpu

    @property
    def words_all(self):
        return sum(self.words_per_user.values())

    @property
    def posts_all(self):
        return len(self.posts)

    def levels_per_user(self, n_words=1500.):
        lpu = {}
        for user in self.words_per_user:
            word_count = self.words_per_user[user]
            lpu[user] = int(self.words_all/n_words)
        return lpu

    def dollars_per_user(self, n_words=10.):
        dpu = {}
        for user in self.words_per_user:
            word_count = self.words_per_user[user]
            post_count = self.posts_per_user[user]
            dpu[user] = int((
                (word_count/n_words)
                - (post_count * 10)
            ))
        return dpu

    def printout(self, words_per_level=1500., words_per_dollar=10.):
        print_list = [
            'Total number of posts: {n_posts}'.format(n_posts=self.posts_all),
            'Total number of words: {n_words}'.format(n_words=self.words_all)
        ]
        lpu = self.levels_per_user(n_words=words_per_level)
        dpu = self.dollars_per_user(n_words=words_per_dollar)
        for user in set(self.users):
            print_list.extend([
                user.upper(),
                '\tNumber of posts: {n_posts}'.format(
                    n_posts=self.posts_per_user[user]
                ),
                '\tNumber of words: {n_words}'.format(
                    n_words=self.words_per_user[user]
                ),
                '\tLevels earned: {n_levels}'.format(
                    n_levels=lpu[user] if self.words_per_user[user] >= 750 else 0
                ),
                '\tPokédollars earned: {n_dollars}'.format(
                    n_dollars=dpu[user] if dpu[user] > 0 else 0
                )
            ])
        return '\n'.join(print_list)
